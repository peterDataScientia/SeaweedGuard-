"""E18 acquisition and eligibility audit; no tuning on external data."""
import sys, json, hashlib, tarfile, zipfile, io
from pathlib import Path
import requests
import pandas as pd
import numpy as np

out=Path(sys.argv[1])/'E18_external'
out.mkdir(parents=True,exist_ok=True)
doi='10.22000/1820'
archive=out/'microplastix.tar'
if not archive.exists():
    landing=requests.get('https://doi.org/'+doi,timeout=120)
    landing.raise_for_status()
    url=landing.links.get('item',{}).get('url')
    if not url: raise RuntimeError('RADAR item link unavailable; inspect DOI landing response')
    tmp=archive.with_suffix('.part')
    with requests.get(url,stream=True,timeout=(30,180)) as response:
        response.raise_for_status()
        with tmp.open('wb') as f:
            for chunk in response.iter_content(1024*1024): f.write(chunk)
    if not tarfile.is_tarfile(tmp): raise ValueError('Download is not a TAR archive')
    tmp.rename(archive)
with tarfile.open(archive) as tar:
    members=tar.getmembers()
    def member(name):
        hits=[m for m in members if m.isfile() and Path(m.name).name==name]
        if len(hits)!=1: raise ValueError(f'Expected one {name}, got {len(hits)}')
        return tar.extractfile(hits[0]).read()
    md=member('metadata.json')
    spectra=member('spectra.zip')
(out/'metadata.json').write_bytes(md)
meta=pd.read_json(io.BytesIO(md),orient='table')
required={'file','Analysis','Polymer','Treatment','Region','Campaign','State','Exposure_days','Polymer_ID','x_unit','y_unit'}
assert required.issubset(meta.columns),required-set(meta.columns)
assert not meta.file.duplicated().any(),'Duplicate metadata filenames'
meta.to_csv(out/'all_metadata.csv',index=False)
atr=meta[meta.Analysis.astype(str).str.strip().str.lower().eq('atr')].copy()
assert len(atr)>0
atr.to_csv(out/'atr_metadata.csv',index=False)
cols=['Polymer','Treatment','State','x_unit','y_unit']
atr.groupby(cols,dropna=False).size().rename('n').reset_index().to_csv(out/'eligibility_summary.csv',index=False)
with zipfile.ZipFile(io.BytesIO(spectra)) as z:
    byname={}
    for name in z.namelist():
        if name.endswith('.csv'):
            base=Path(name).name
            if base in byname: raise ValueError('Duplicate spectrum basename '+base)
            byname[base]=name
    records=[]
    for row in atr.itertuples(index=False):
        name=str(row.file)
        if Path(name).name!=name or name not in byname:
            records.append({'file':name,'status':'missing spectrum'})
            continue
        data=z.read(byname[name])
        try:
            d=pd.read_csv(io.BytesIO(data))
            a=d.apply(pd.to_numeric,errors='raise').to_numpy(float)
            assert a.ndim==2 and a.shape[1]==2 and len(a)>=11 and np.isfinite(a).all()
            x=np.sort(a[:,0])
            assert np.all(np.diff(x)>0)
            records.append({'file':name,'status':'parsed','n':len(x),'xmin':x[0],'xmax':x[-1],'sha256':hashlib.sha256(data).hexdigest(),'axis_header':str(d.columns[0]),'signal_header':str(d.columns[1])})
        except Exception as e:
            records.append({'file':name,'status':'invalid: '+str(e)})
    audit=pd.DataFrame(records)
    audit.to_csv(out/'spectrum_audit.csv',index=False)
    parsed=audit[audit.status.eq('parsed')]
    folder=out/'atr_spectra';folder.mkdir(exist_ok=True)
    for name in parsed.file:
        (folder/name).write_bytes(z.read(byname[name]))
manifest={'doi':doi,'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'metadata_rows':len(meta),'atr_rows':len(atr),'parsed_atr':len(parsed),'status':'ACQUIRED_NOT_SCORED','license':'CC BY-SA 4.0'}
(out/'acquisition.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(manifest,indent=2))
print(atr.groupby(cols,dropna=False).size().to_string())
print('E18 PAUSED: verify label, treatment, intensity units, specimen grouping and reference overlap before scoring. Frozen parameters unchanged.')
