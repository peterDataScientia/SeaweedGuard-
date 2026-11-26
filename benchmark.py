import numpy as np,pandas as pd,json,sys
from pathlib import Path
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold,cross_val_predict
from sklearn.metrics import balanced_accuracy_score,f1_score,confusion_matrix
from screening import preprocess
import joblib

def main(data,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    d=pd.read_csv(Path(data)/'clean_index.csv');z=np.load(Path(data)/'clean_spectra.npz')
    assert np.array_equal(z['hash'],d.hash.to_numpy())
    x=preprocess(z['intensity']);y=d.provisional_label.to_numpy()
    tr=(d.condition=='pristine')&d.provisional_label.isin(['PP','PVC']);te=(d.condition!='pristine')&d.provisional_label.isin(['PP','PVC'])
    a,b=x[tr],y[tr];c,t=x[te],y[te];labels=['PP','PVC'];cv=StratifiedKFold(5,shuffle=True,random_state=2024);results=[]
    preds=d.loc[te,['path','condition','provisional_label']].copy()
    def report(name,split,truth,pred):
        results.append(dict(model=name,split=split,n=len(truth),balanced_accuracy=balanced_accuracy_score(truth,pred),macro_f1=f1_score(truth,pred,labels=labels,average='macro'),confusion=confusion_matrix(truth,pred,labels=labels).tolist()))
    oof=np.empty(len(b),dtype=object);score=np.empty(len(b))
    for i,j in cv.split(a,b):
        sim=a[j]@a[i].T;k=sim.argmax(1);oof[j]=b[i][k];score[j]=sim.max(1)
    report('correlation_1NN','pristine_row_cv',b,oof);threshold=float(np.quantile(score,.05))
    sim=c@a.T;pred=b[sim.argmax(1)];conf=sim.max(1);report('correlation_1NN','exposed',t,pred)
    preds['correlation']=pred;preds['similarity']=conf;preds['accepted']=conf>=threshold
    for name,model in [('SVM',SVC(C=10,gamma='scale')),('RF',RandomForestClassifier(n_estimators=200,random_state=2024,n_jobs=2))]:
        report(name,'pristine_row_cv',b,cross_val_predict(model,a,b,cv=cv));model.fit(a,b);p=model.predict(c);report(name,'exposed',t,p);preds[name]=p;joblib.dump(model,out/(name+'.joblib'))
    accepted=conf>=threshold
    summary=dict(train_n=len(b),test_n=len(t),threshold=threshold,coverage=float(accepted.mean()),accepted_accuracy=float((pred[accepted]==t[accepted]).mean()) if accepted.any() else None,results=results,limitations='Provisional labels; specimen independence unknown; row CV diagnostic only; PP/PVC closed set; heuristic threshold; no official OpenSpecy comparison.')
    (out/'metrics.json').write_text(json.dumps(summary,indent=2));preds.to_csv(out/'predictions.csv',index=False)
    np.savez_compressed(out/'reference.npz',x=a,y=b.astype(str),wavenumber=z['wavenumber'],threshold=threshold)
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main(*sys.argv[1:])
