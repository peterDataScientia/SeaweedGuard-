import numpy as np
import pytest
from spectral_units import display_signal, input_absorbance, preview_spectrum

def test_reversible_display_units():
    a=np.array([0.,.1,.5,1.,2.])
    original=a.copy()
    np.testing.assert_allclose(display_signal(a,"% Absorbance"),a*100)
    np.testing.assert_allclose(display_signal(a,"% Transmittance"),100*10**(-a))
    np.testing.assert_allclose(input_absorbance(display_signal(a,"% Absorbance"),"percent absorbance"),a)
    np.testing.assert_allclose(input_absorbance(display_signal(a,"% Transmittance"),"percent transmittance"),a,atol=1e-14)
    np.testing.assert_array_equal(a,original)

def test_preview_and_bad_transmittance():
    x=np.arange(1000.,1012.)
    a=np.linspace(.1,.5,len(x))
    xx,aa=preview_spectrum(np.column_stack([x[::-1],a[::-1]*100]),"percent absorbance")
    np.testing.assert_allclose(xx,x)
    np.testing.assert_allclose(aa,a)
    for value in [0.,-1.,101.]:
        with pytest.raises(ValueError): input_absorbance([value],"percent transmittance")
