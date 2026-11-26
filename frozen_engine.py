import numpy as np
from scipy.signal import savgol_filter
CLASSES=np.array(['Nylon','PP','PS','PVC','Other'])
SIM=0.879220
MARGIN=0.058389

def preprocess(a,grid):
    a=np.asarray(a,dtype=float)
    d=savgol_filter(np.atleast_2d(a),11,2,deriv=1,axis=1)[:,~((grid>=1500)&(grid<1700))]
    d-=d.mean(1,keepdims=True)
    n=np.linalg.norm(d,axis=1,keepdims=True)
    if not np.isfinite(d).all() or (n<=1e-12).any(): raise ValueError('Invalid or flat spectrum')
    return d/n

def load_model(file):
    with np.load(file,allow_pickle=False) as z:
        g,a,y,ids=(z[k] for k in ('grid','reference','labels','ids'))
    if len(g)!=750 or len(ids)!=459 or len(set(ids))!=459 or set(y)!=set(CLASSES) or (y!='Other').sum()!=154 or a.shape!=(459,(~((g>=1500)&(g<1700))).sum()) or not np.isfinite(a).all() or not np.isfinite(g).all() or not np.all(np.diff(g)>0) or not np.allclose(np.linalg.norm(a,axis=1),1): raise ValueError('Incompatible E18 model bundle')
    return g,a,y,ids

def screen(data,model,unit='absorbance'):
    g,a,y,ids=model
    v=np.asarray(data,dtype=float)
    if v.ndim!=2 or v.shape[1]!=2 or len(v)<11 or not np.isfinite(v).all(): raise ValueError('Expected two finite numeric columns')
    v=v[np.argsort(v[:,0])];x,s=v.T
    if unit=='percent absorbance': s=s/100
    elif unit=='percent transmittance':
        if (s<=0).any() or (s>100).any(): raise ValueError('Invalid percent transmittance')
        s=-np.log10(s/100)
    elif unit!='absorbance': raise ValueError('Unknown units')
    inside=x[(x>=g[0])&(x<=g[-1])]
    if np.any(np.diff(x)<=0) or x[0]>g[0] or x[-1]<g[-1] or len(inside)<2 or np.max(np.diff(inside))>2*np.median(np.diff(g)): raise ValueError('Insufficient or incompatible wavenumber coverage')
    signal=np.interp(g,x,s); scores=(preprocess(signal,g)@a.T)[0]
    cm=np.array([scores[y==k].max() for k in CLASSES]);order=np.argsort(cm);j=order[-1];candidate=str(CLASSES[j]);similarity=float(cm[j]);margin=float(cm[j]-cm[order[-2]])
    accepted=bool(candidate!='Other' and similarity>=SIM and margin>=MARGIN)
    return dict(candidate=candidate,similarity=similarity,margin=margin,accepted=accepted,status='Accepted candidate' if accepted else 'Non-target candidate' if candidate=='Other' else 'Tentative candidate',reference_id=str(ids[scores.argmax()]),signal=signal)
