import argparse, hashlib, io, zipfile
from pathlib import Path
import numpy as np
import pandas as pd

p=argparse.ArgumentParser();p.add_argument('archive');p.add_argument('--out',default='outputs/E02');args=p.parse_args()
out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
rows=[]; arrays={}
with zipfile.ZipFile(args.archive) as z:
 for library,filename in [('test','Test_spectra_library.zip'),('bio','Biofouled_spectra_library.zip')]:
  with zipfile.ZipFile(io.BytesIO(z.read(filename))) as a:
   for name in sorted(a.namelist()):
    if not name.lower().endswith('.csv'): continue
    folder=name.split('/')[1];v=np.loadtxt(io.BytesIO(a.read(name)),delimiter=',',skiprows=1,dtype='<f8');h=hashlib.sha256(v.tobytes()).hexdigest()
    if library=='test': label=folder;condition='pristine'
    else:
     label={'nylon':'Nylon_fragments','pp':'PP','ps':'PS','pvc':'PVC'}[folder.split('_')[0].lower()];condition='pristine' if 'pristine' in folder.lower() else 'exposed_'+folder.split('_')[-1].lower()
    rows.append(dict(path=name,library=library,folder=folder,provisional_label=label,condition=condition,hash=h,valid_axis=bool(len(v)==863 and np.isfinite(v).all() and np.all(np.diff(v[:,0])>0))))
    arrays[h]=v
m=pd.DataFrame(rows);grid=arrays[m.loc[m.valid_axis,'hash'].iloc[0]][:,0]
m['valid_axis']=[ok and np.array_equal(arrays[h][:,0],grid) for ok,h in zip(m.valid_axis,m.hash)]
m['label_conflict']=m.groupby('hash').provisional_label.transform('nunique')>1
m['condition_conflict']=m.groupby('hash').condition.transform('nunique')>1
m['status']='eligible';m.loc[m.label_conflict|m.condition_conflict,'status']='quarantine_conflict';m.loc[~m.valid_axis,'status']='quarantine_axis'
valid=m[m.status.eq('eligible')].sort_values(['library','path'],ascending=[False,True]);keep=valid.drop_duplicates('hash');m.loc[valid.index.difference(keep.index),'status']='redundant_copy'
keep=keep.copy();keep['partition']=np.where(keep.condition.eq('pristine'),'pristine_pool','exposed_holdout')
assert set(keep[keep.partition=='pristine_pool'].hash).isdisjoint(keep[keep.partition=='exposed_holdout'].hash)
m.to_csv(out/'manifest.csv',index=False);keep.to_csv(out/'clean_index.csv',index=False)
np.savez_compressed(out/'clean_spectra.npz',wavenumber=grid,intensity=np.stack([arrays[h][:,1] for h in keep.hash]),hash=keep.hash.to_numpy(dtype=str))
print(m.status.value_counts());print(keep.groupby(['provisional_label','condition']).size().unstack(fill_value=0));print(keep.partition.value_counts());print('conflicting groups',m.loc[m.label_conflict,'hash'].nunique(),'condition conflicts',m.loc[m.condition_conflict,'hash'].nunique());print('quarantine unique',m.loc[m.status.str.startswith('quarantine'),'hash'].nunique())
