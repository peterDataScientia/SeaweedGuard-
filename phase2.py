import sys,json
from pathlib import Path
import numpy as np,pandas as pd
from scipy.sparse.csgraph import connected_components
from sklearn.model_selection import StratifiedKFold, StratifiedGroupKFold
from sklearn.metrics import balanced_accuracy_score,f1_score
from sklearn.svm import SVC
from screening import preprocess

def main(data,out):
 d=pd.read_csv(Path(data)/'clean_index.csv');z=np.load(Path(data)/'clean_spectra.npz');assert np.array_equal(z['hash'],d.hash.to_numpy())
 x=preprocess(z['intensity']);y=d.provisional_label.to_numpy();tr=d.condition.eq('pristine').to_numpy();te=~tr
 a,b=x[tr],y[tr];c,t=x[te],y[te];sim=a@a.T
 results=[];counts=pd.Series(b).value_counts();eligible=np.isin(b,counts[counts>=5].index)
 def evaluate(name,truth,pred):
  results.append(dict(test=name,n=len(truth),accuracy=float(np.mean(truth==pred)),balanced_accuracy=balanced_accuracy_score(truth,pred),macro_f1=f1_score(truth,pred,labels=np.unique(truth),average='macro',zero_division=0)))
 def cv_run(splitter,name,groups=None):
  q=a[eligible];r=b[eligible];p=np.empty(len(r),dtype=object);s=p.copy()
  for i,j in splitter.split(q,r,groups):
   p[j]=r[i][(q[j]@q[i].T).argmax(1)];s[j]=SVC(C=10,gamma='scale').fit(q[i],r[i]).predict(q[j])
  evaluate(name+'_1NN',r,p);evaluate(name+'_SVM',r,s)
 cv_run(StratifiedKFold(5,shuffle=True,random_state=2024),'row_CV')
 group_info=[]
 for cutoff in [.999,.995,.99]:
  _,g=connected_components(sim>=cutoff,directed=False);gg=g[eligible];group_info.append(dict(cutoff=cutoff,groups=len(set(gg)),minimum_groups_per_class=int(pd.DataFrame({'y':b[eligible],'g':gg}).groupby('y').g.nunique().min())))
  cv_run(StratifiedGroupKFold(5,shuffle=True,random_state=2024),f'group_CV_{cutoff}',gg)
 s=c@a.T;p=b[s.argmax(1)];evaluate('exposed_18class_1NN',t,p);evaluate('exposed_18class_SVM',t,SVC(C=10,gamma='scale').fit(a,b).predict(c))
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 pd.DataFrame({'truth':t,'candidate':p,'similarity':s.max(1)}).to_csv(out/'phase2_exposed_predictions.csv',index=False)
 outj=dict(pristine=len(a),exposed=len(c),classes=len(counts),cv_classes=int(counts.ge(5).sum()),counts=counts.to_dict(),groups=group_info,metrics=results,exposed_by_class=pd.crosstab(t,p).to_dict(),exposed_near_reference={str(v):int((s.max(1)>=v).sum()) for v in [.999,.995,.99]})
 (out/'phase2_metrics.json').write_text(json.dumps(outj,indent=2));print(json.dumps(outj,indent=2))
if __name__=='__main__':main(*sys.argv[1:])
