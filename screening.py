import numpy as np
from scipy.signal import savgol_filter

def preprocess(x):
    x=savgol_filter(np.atleast_2d(np.asarray(x,dtype=float)),11,2,deriv=1,axis=1)
    x-=x.mean(axis=1,keepdims=True)
    n=np.linalg.norm(x,axis=1,keepdims=True)
    if np.any(n<=1e-12): raise ValueError('Flat or uninformative spectrum')
    return x/n

def screen(a, reference):
    a=np.asarray(a,dtype=float)
    if a.ndim!=2 or a.shape[1]!=2 or len(a)<11 or not np.isfinite(a).all(): raise ValueError('Expected two finite numeric columns and at least 11 rows')
    a=a[np.argsort(a[:,0])];g=reference['wavenumber'];dx=np.diff(a[:,0])
    if np.any(dx<=0) or a[0,0]>g.min() or a[-1,0]<g.max(): raise ValueError('Duplicate axis values or insufficient spectral coverage')
    if np.max(dx)>2*np.median(np.diff(g)): raise ValueError('Spectral grid too sparse')
    v=np.interp(g,a[:,0],a[:,1]);s=(preprocess(v)@reference['x'].T)[0];j=int(s.argmax());score=float(s[j])
    return dict(candidate=str(reference['y'][j]),similarity=score,accepted=bool(score>=float(reference['threshold'])),signal=v)
