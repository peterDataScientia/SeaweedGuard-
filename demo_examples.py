"""Experimental examples, independent of proprietary/reference bundle."""
from pathlib import Path
import json
import zlib
import base64
import numpy as np
from spectral_units import input_absorbance

def decode(value,scale):
    raw=zlib.decompress(base64.b64decode(value,validate=True))
    values=np.frombuffer(raw,dtype="<i2")
    if values.size!=750: raise ValueError("Example spectrum damaged")
    return np.cumsum(values,dtype=np.int64)/scale

def load_examples():
    data=json.loads((Path(__file__).resolve().parent/"assets/demo_data.json").read_text())
    grid=np.round(data["grid_start"]+decode(data["grid"],1000),3)
    examples={}
    for row in data["examples"]:
        example={k:v for k,v in row.items() if k!="data"}
        example["signal"]=decode(row["data"],100000)
        examples[row["name"]]=example
    assert np.all(np.diff(grid)>0) and len(examples)==4
    return grid,examples

def demo_status(result):
    if result["accepted"]: return "Accepted candidate · confirmation as required"
    if result["candidate"]=="Other": return "Non-target candidate"
    return "Tentative candidate · review required"


def example_csv(grid, example):
    import pandas as pd
    return pd.DataFrame({"wavenumber":grid,"absorbance":example["signal"]}).to_csv(index=False).encode("utf-8")

def match_uploaded_example(data, unit="absorbance"):
    """Recognize only the bundled numerical spectra; never replay arbitrary uploads."""
    data=np.asarray(data,dtype=float)
    grid,examples=load_examples()
    if data.shape!=(len(grid),2) or not np.isfinite(data).all():
        return None
    data=data[np.argsort(data[:,0])]
    if not np.allclose(data[:,0],grid,rtol=0,atol=1e-9):
        return None
    try:
        signal=input_absorbance(data[:,1],unit)
    except ValueError:
        return None
    for example in examples.values():
        if np.allclose(signal,example["signal"],rtol=0,atol=1e-10):
            return grid,example
    return None
