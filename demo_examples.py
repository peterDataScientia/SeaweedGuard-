"""Experimental examples, independent of proprietary/reference bundle."""
from pathlib import Path
import json
import zlib
import base64
import numpy as np

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
