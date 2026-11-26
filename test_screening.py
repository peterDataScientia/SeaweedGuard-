import numpy as np,pytest
from screening import screen,preprocess

def ref():
    g=np.linspace(675,4000,863);v=np.sin(g/50);w=np.cos(g/35)
    return dict(wavenumber=g,x=preprocess([v,w]),y=np.array(['PP','PVC']),threshold=.9652),v

def test_known():
    r,v=ref();res=screen(np.c_[r['wavenumber'],v],r);assert res['candidate']=='PP' and res['accepted']
def test_reverse():
    r,v=ref();assert screen(np.c_[r['wavenumber'],v][::-1],r)['accepted']
def test_unknown():
    r,v=ref();assert not screen(np.c_[r['wavenumber'],np.sin(r['wavenumber']/12)],r)['accepted']
@pytest.mark.parametrize('kind',['flat','missing','duplicate','short','sparse'])
def test_invalid(kind):
    r,v=ref();a=np.c_[r['wavenumber'],v]
    if kind=='flat':a[:,1]=0
    if kind=='missing':a[5,1]=np.nan
    if kind=='duplicate':a[5,0]=a[4,0]
    if kind=='short':a=a[10:]
    if kind=='sparse':a=a[::5];a=np.vstack([a,[r['wavenumber'][-1],v[-1]]])
    with pytest.raises(ValueError):screen(a,r)
