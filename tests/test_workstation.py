from pathlib import Path
from streamlit.testing.v1 import AppTest

APP=Path(__file__).resolve().parents[1]/"app.py"

def test_analyzer_starts_without_model():
    at=AppTest.from_file(str(APP),default_timeout=30).run()
    assert not at.exception
    assert at.sidebar.radio[0].value=="Analyzer"
    assert at.button[0].disabled

def test_navigation_without_model():
    at=AppTest.from_file(str(APP),default_timeout=30).run()
    for page in ["Batch analysis","Reference library","Farm monitoring","History","Settings","About","Analyzer"]:
        at.sidebar.radio[0].set_value(page).run()
        assert not at.exception, (page,at.exception)
