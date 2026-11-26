from pathlib import Path
from streamlit.testing.v1 import AppTest
from demo_examples import load_examples,demo_status

APP=Path(__file__).resolve().parents[1]/"app.py"

def test_example_data():
    g,examples=load_examples()
    assert len(g)==750
    assert [x["candidate"] for x in examples.values()]==["PP","PS","PP","Other"]
    assert [x["accepted"] for x in examples.values()]==[True,True,False,False]

def test_demo_without_model():
    at=AppTest.from_file(str(APP),default_timeout=30).run()
    assert not at.exception
    assert at.sidebar.radio[0].value=="Analyzer"
    assert at.button(key="demo_run").disabled
    at.button[0].click().run()
    assert not at.exception
    at.button(key="demo_run").click().run()
    assert not at.exception
    assert at.metric[0].value=="PP"
    at.button(key="demo_clear").click().run()
    assert not at.exception
    assert at.button(key="demo_run").disabled

def test_navigation_without_model():
    at=AppTest.from_file(str(APP),default_timeout=30).run()
    for page in ["Batch analysis","Reference library","Farm monitoring","History","Settings","About","Analyzer"]:
        at.sidebar.radio[0].set_value(page).run()
        assert not at.exception, (page,at.exception)


def test_downloaded_examples_round_trip():
    import pandas as pd
    from io import BytesIO
    from demo_examples import example_csv,match_uploaded_example
    g,examples=load_examples()
    for ex in examples.values():
        arr=pd.read_csv(BytesIO(example_csv(g,ex))).to_numpy(float)
        match=match_uploaded_example(arr)
        assert match is not None and match[1]["file"]==ex["file"]
        assert match_uploaded_example(arr[::-1])[1]["file"]==ex["file"]
        assert match_uploaded_example(arr,"percent absorbance") is None
        arr[10,1]+=.001
        assert match_uploaded_example(arr) is None
