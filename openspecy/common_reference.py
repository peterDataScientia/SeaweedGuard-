"""E13: same reference identities; compare pipelines, not just algorithms."""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from scipy.stats import binomtest
from sklearn.svm import SVC
from sklearn.metrics import balanced_accuracy_score, f1_score

out=Path(sys.argv[1])
common=out/'common_reference'
ref=pd.read_csv(common/'raw_reference.csv')
meta=pd.read_csv(common/'reference_metadata.csv').set_index('sample_name',verify_integrity=True)
truth=pd.read_csv(out/'truth.csv').set_index('hash',verify_integrity=True)
matches=pd.read_csv(out/'matches.csv')
ids=ref.columns[1:].tolist()
assert len(ids)==459 and set(ids)==set(meta.index)
assert len(truth)==232 and set(matches.query_id)==set(truth.index)
assert matches.groupby('query_id').size().eq(5).all()
assert set(matches.library_id).issubset(ids)
def reference_label(row):
    def norm(v):
        return str(v).strip().lower()
    m,c,i=map(norm,(row['material'],row['material_class'],row['spectrum_identity']))
    if 'aramid' in i or 'kevlar' in m or 'terephthalamide' in m:
        return 'Other:aramid'
    if c=='polyamides' and (m.startswith(('nylon','polyamide')) or i.startswith(('nylon','polyamide','pa '))):
        return 'Nylon'
    if m in ('pp','polypropylene','poly(propylene)'): return 'PP'
    if m in ('ps','polystyrene','poly(styrene)'): return 'PS'
    if m in ('pvc','polyvinylchloride','polyvinyl chloride','poly(vinyl chloride)'): return 'PVC'
    return 'Other:'+(c if m in ('nan','','none','other','other plastic','other material') else m)
def prep(x):
    x=savgol_filter(np.asarray(x,dtype=float),11,2,deriv=1,axis=1)
    x-=x.mean(axis=1,keepdims=True)
    n=np.linalg.norm(x,axis=1,keepdims=True)
    if not np.isfinite(x).all() or (n<=1e-12).any(): raise ValueError('Invalid derivative spectrum')
    return x/n
queries=[pd.read_csv(out/'queries'/f'{i}.csv') for i in truth.index]
rx=ref.wavenumber.to_numpy(float)
order=np.argsort(rx);rx=rx[order]
rv=ref[ids].to_numpy(float)[order]
assert np.all(np.diff(rx)>0)
# Use the intersection of native spectral ranges, no extrapolation.
valid=np.isfinite(rv).all(axis=1)
blocks=np.split(np.flatnonzero(valid),np.flatnonzero(np.diff(np.flatnonzero(valid))>1)+1)
block=max(blocks,key=len)
assert len(block)>=11,'No complete common spectral interval'
rx=rx[block];rv=rv[block]
lo=max(rx.min(),max(q.wavenumber.min() for q in queries))
hi=min(rx.max(),min(q.wavenumber.max() for q in queries))
grid=np.sort(queries[0].wavenumber.to_numpy(float))
grid=grid[(grid>=lo)&(grid<=hi)]
assert len(grid)>=11
assert np.isfinite(rv).all(), 'Raw library contains missing/nonfinite intensities; inspect before proceeding'
a=prep(np.array([np.interp(grid,rx,rv[:,i]) for i in range(len(ids))]))
rows=[]
for q in queries:
    q=q.sort_values('wavenumber')
    assert np.all(np.diff(q.wavenumber)>0)
    rows.append(np.interp(grid,q.wavenumber,q.absorbance))
b=prep(np.array(rows))
y=meta.loc[ids].apply(reference_label,axis=1).to_numpy()
t=truth.provisional_label.map(lambda x:'Nylon' if str(x).startswith('Nylon') else x)
assert set(t)=={'Nylon','PP','PS','PVC'}
sim=b@a.T
best=sim.argmax(axis=1)
p1=y[best]
p2=SVC(C=10,gamma='scale').fit(a,y).predict(b)
top=matches.sort_values(['query_id','match_val','library_id'],ascending=[True,False,True]).drop_duplicates('query_id').set_index('query_id').loc[truth.index]
def collapse(x): return np.array(['Other' if str(v).startswith('Other:') else v for v in x])
res=pd.DataFrame({'truth':t,'condition':truth.condition,'OpenSpecy':collapse(top.apply(reference_label,axis=1)),'SG_1NN':collapse(p1),'SG_SVM':collapse(p2),'SG_reference_id':np.array(ids)[best],'SG_similarity':sim.max(axis=1),'OpenSpecy_similarity':top.match_val},index=truth.index)
labels=['Nylon','PP','PS','PVC']
common=common/'E14_corrected'
common.mkdir(exist_ok=True)
metrics=[]
for name in ['OpenSpecy','SG_1NN','SG_SVM']:
    pred=res[name]
    metrics.append({'method':name,'n':len(res),'correct':int((pred==t).sum()),'accuracy':float((pred==t).mean()),'balanced_accuracy':balanced_accuracy_score(t,pred),'macro_f1_target':f1_score(t,pred,labels=labels,average='macro',zero_division=0)})
    pd.crosstab(t,pred).reindex(index=labels,columns=labels+['Other'],fill_value=0).to_csv(common/f'confusion_{name}.csv')
paired=[]
for name in ['SG_1NN','SG_SVM']:
    aok=res[name].eq(t);bok=res.OpenSpecy.eq(t)
    x=int((aok&~bok).sum());z=int((~aok&bok).sum())
    paired.append({'method':name,'both_correct':int((aok&bok).sum()),'SG_only':x,'OpenSpecy_only':z,'both_incorrect':int((~aok&~bok).sum()),'exact_mcnemar_p':binomtest(x,x+z,.5).pvalue if x+z else 1.0})
meta.assign(mapped_label=meta.apply(reference_label,axis=1)).reset_index()[['sample_name','material','material_class','spectrum_identity','mapped_label']].to_csv(common/'reference_label_mapping.csv',index=False)
res.to_csv(common/'paired_predictions.csv')
pd.DataFrame(metrics).to_csv(common/'metrics.csv',index=False)
pd.DataFrame(paired).to_csv(common/'paired_tests.csv',index=False)
meta.material.value_counts().to_csv(common/'material_counts.csv')
print('Shared raw reference IDs:',len(ids),'query IDs:',len(truth),'grid:',grid.min(),grid.max(),len(grid))
print(pd.DataFrame(metrics).to_string(index=False))
print(pd.DataFrame(paired).to_string(index=False))
print('Exploratory: preprocessing and grid differ; source-level independence does not prove specimen independence.')
