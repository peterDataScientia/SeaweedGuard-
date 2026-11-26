import json,sys
from pathlib import Path
import numpy as np,pandas as pd
from screening import preprocess

def main(data,results):
    data=Path(data);results=Path(results)
    d=pd.read_csv(data/'clean_index.csv');z=np.load(data/'clean_spectra.npz');r=np.load(results/'reference.npz')
    assert np.array_equal(z['hash'],d.hash.to_numpy())
    neg=~d.provisional_label.isin(['PP','PVC']);s=preprocess(z['intensity'][neg])@r['x'].T
    q=d.loc[neg,['path','condition','provisional_label','hash']].copy();q['candidate']=r['y'][s.argmax(1)];q['similarity']=s.max(1);q['accepted']=q.similarity>=float(r['threshold'])
    q.to_csv(results/'unknown_predictions.csv',index=False)
    q.groupby('provisional_label').accepted.agg(['size','sum']).to_csv(results/'unknown_by_class.csv')
    summary=dict(n=len(q),false_accepts=int(q.accepted.sum()),rejected=int((~q.accepted).sum()),false_accept_rate=float(q.accepted.mean()),threshold=float(r['threshold']))
    (results/'unknown_metrics.json').write_text(json.dumps(summary,indent=2));print(summary)
if __name__=='__main__':main(*sys.argv[1:])
