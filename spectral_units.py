"""Spectral units for display and file interpretation, separate from frozen inference."""
import numpy as np

UNITS=("Absorbance","% Absorbance","% Transmittance")

def display_signal(absorbance, unit):
    a=np.asarray(absorbance,dtype=float)
    if unit==UNITS[0]: return a.copy()
    if unit==UNITS[1]: return a*100
    if unit==UNITS[2]:
        with np.errstate(over="raise",invalid="ignore"):
            return 100*np.power(10.,-a)
    raise ValueError("Unknown display unit")

def input_absorbance(signal, unit):
    s=np.asarray(signal,dtype=float)
    if not np.isfinite(s).all(): raise ValueError("Nonfinite intensity")
    if unit=="absorbance": return s.copy()
    if unit=="percent absorbance": return s/100
    if unit=="percent transmittance":
        if np.any((s<=0)|(s>100)): raise ValueError("Transmittance must be > 0 and ≤ 100")
        return -np.log10(s/100)
    raise ValueError("Unknown CSV intensity unit")

def preview_spectrum(data,unit):
    a=np.asarray(data,dtype=float)
    if a.ndim!=2 or a.shape[1]!=2 or len(a)<11 or not np.isfinite(a).all():
        raise ValueError("Expected two finite numeric columns and at least 11 rows")
    a=a[np.argsort(a[:,0])]
    if np.any(np.diff(a[:,0])<=0): raise ValueError("Duplicate wavenumbers")
    return a[:,0],input_absorbance(a[:,1],unit)
