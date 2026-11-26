import streamlit as st
import pandas as pd
from pathlib import Path
from frozen_engine import load_model, screen, SIM, MARGIN

st.set_page_config(page_title="SeaweedGuard",page_icon="🌊",layout="wide")
st.sidebar.title("SeaweedGuard")
st.sidebar.caption("v0.1.0 | Research prototype")
page=st.sidebar.radio("Workspace",["Dashboard","Spectrum screening","Batch screening","Farm monitoring","Validation"])
st.sidebar.caption("ATR-FTIR • Evidence-led polymer screening")
st.title(page)
st.caption("SeaweedGuard | Microplastic monitoring research")
if page=="Dashboard":
    st.info("Screen individual measured ATR-FTIR spectra for four target polymer classes. This is not a food-safety or seaweed-tissue diagnostic.")
    a,b,c=st.columns(3)
    a.metric("Reference spectra",459);b.metric("External ATR spectra",3832);c.metric("External target accuracy","85.37%")
    st.subheader("Workflow")
    st.write("Collect and isolate particles → acquire ATR-FTIR spectrum → screen → expert review → record field observations.")
    st.write("Supported targets: Nylon, PP, PS and PVC. Independent external evaluation covers PP and PS only.")
elif page in ("Spectrum screening","Batch screening"):
    st.warning("Similarity is not a probability. Accepted candidates require appropriate experimental confirmation. Not validated for direct seaweed-tissue analysis.")
    bundle=Path(__file__).parent/"models/frozen_model.npz"
    uploaded=st.file_uploader("Load authorised E18 model bundle (.npz)",type=["npz"]) if not bundle.exists() else None
    if not bundle.exists() and uploaded is None:
        st.info("Supply the frozen model bundle from the project Drive. Reference-derived data are not bundled in the public repository pending licence review.")
        st.stop()
    try: model=load_model(bundle if bundle.exists() else uploaded)
    except Exception as e: st.error(str(e));st.stop()
    unit=st.selectbox("Measured intensity units",["absorbance","percent absorbance","percent transmittance"])
    st.caption("CSV must contain a header and exactly two numeric columns: wavenumber (cm⁻¹), intensity. Do not use Raman spectra.")
    batch=page=="Batch screening"
    files=st.file_uploader("Spectrum CSV files" if batch else "Spectrum CSV",type=["csv"],accept_multiple_files=batch)
    files=files if batch else ([files] if files else [])
    if files:
        rows=[]
        for f in files:
            try:
                r=screen(pd.read_csv(f).to_numpy(float),model,unit)
                rows.append(dict(file=f.name,**{k:v for k,v in r.items() if k!="signal"}))
                if not batch:
                    a,b,c=st.columns(3);a.metric("Candidate",r["candidate"]);b.metric("Similarity",f'{r["similarity"]:.4f}');c.metric("Class margin",f'{r["margin"]:.4f}')
                    st.write(r["status"]);st.line_chart(pd.DataFrame({"absorbance":r["signal"]},index=model[0]),x_label="Wavenumber (cm⁻¹)")
            except Exception as e: rows.append(dict(file=f.name,status="Invalid input",error=str(e)))
        result=pd.DataFrame(rows);st.dataframe(result,hide_index=True)
        st.download_button("Download screening report",result.to_csv(index=False),"seaweedguard_screening.csv","text/csv")
    st.caption(f"Frozen thresholds: similarity ≥ {SIM}; margin ≥ {MARGIN}. Region 1500–1700 cm⁻¹ excluded.")
elif page=="Farm monitoring":
    st.caption("Session-only observations; these do not establish contamination source or intervention efficacy.")
    with st.form("monitor"):
        site=st.text_input("Farm / sample ID");stage=st.selectbox("Stage",["Cultivation","Harvest","Drying","Transport","Processing"]);date=st.date_input("Observation date");note=st.text_area("Observation or possible contamination source");submit=st.form_submit_button("Record")
    if "records" not in st.session_state: st.session_state.records=[]
    if submit and site.strip(): st.session_state.records.append(dict(sample=site,stage=stage,date=str(date),observation=note))
    if st.session_state.records:
        table=pd.DataFrame(st.session_state.records);st.dataframe(table,hide_index=True);st.download_button("Export monitoring log",table.to_csv(index=False),"farm_log.csv","text/csv")
else:
    st.subheader("E18 | MicroPlastiX external evaluation")
    st.write("Frozen model; DOI: 10.22000/1820. Spectrum-level metrics, not independent specimen counts.")
    st.table(pd.DataFrame({"Metric":["PP/PS target identification","Accepted target accuracy","Target coverage","Non-target rejection"],"Result":["1027/1203 (85.37%)","767/767 (100%)","767/1203 (63.76%)","2615/2629 (99.47%)"]}))
    st.warning("Nylon and PVC were absent from this external dataset. No direct seaweed-tissue validation. Accepted target accuracy excludes non-target false acceptances.")
    st.write("Non-target refers to polymers outside the four supported classes, not necessarily non-plastics.")
