"""SeaweedGuard v0.2.4 — spectral workstation. Frozen E18 engine unchanged."""
import hashlib
from io import BytesIO
from pathlib import Path
from datetime import datetime
import numpy as np
import pandas as pd
import streamlit as st
from frozen_engine import load_model, screen, preprocess, CLASSES, SIM, MARGIN

BASE=Path(__file__).resolve().parent
st.set_page_config(page_title="SeaweedGuard | Spectral Workstation",page_icon="🌊",layout="wide",initial_sidebar_state="expanded")
st.markdown((BASE/"assets/workstation.css").read_text(),unsafe_allow_html=True)
for key,default in {"runs":{},"history":[],"farm":[]}.items():
    if key not in st.session_state: st.session_state[key]=default

@st.cache_resource
def open_bundle(raw):
    return load_model(BytesIO(raw))

with st.sidebar:
    st.markdown('<div class="sg-brand">Seaweed<span>Guard</span></div><div class="sg-kicker">SPECTRAL WORKSTATION / 02</div>',unsafe_allow_html=True)
    st.divider()
    page=st.radio("WORKSPACE",["Analyzer","Batch analysis","Reference library","Farm monitoring","History","Settings","About"],index=0)
    st.divider()
    st.caption("MODEL")
    installed=BASE/"models/frozen_model.npz"
    uploaded=None if installed.exists() else st.file_uploader("Connect model",type=["npz"],key="model",help="Select the authorised E18 frozen model bundle.")
    raw=installed.read_bytes() if installed.exists() else uploaded.getvalue() if uploaded else None
    model=None
    model_error=None
    if raw is not None:
        try: model=open_bundle(raw)
        except Exception as exc: model_error=str(exc)
    if model is not None: st.caption("● Connected · 459 references")
    elif model_error: st.error("Model rejected: "+model_error)
    else: st.caption("○ Not connected")
    st.caption("v0.2.4  /  E18 FROZEN")

ready=model is not None
model_id=hashlib.sha256(raw).hexdigest() if ready else None
titles={"Analyzer":("01 / SPECTRAL WORKSPACE","Spectrum analyzer"),"Batch analysis":("02 / HIGH-THROUGHPUT","Batch analysis"),"Reference library":("03 / REFERENCE SYSTEM","Reference library"),"Farm monitoring":("04 / FIELD WORKSPACE","Farm monitoring"),"History":("05 / SESSION RECORDS","Analysis history"),"Settings":("06 / CONFIGURATION","Instrument settings"),"About":("07 / DOCUMENTATION","Scientific documentation")}
k,t=titles[page]
status="LIVE ENGINE" if ready else "DEMO AVAILABLE" if page=="Analyzer" else "MODEL OFFLINE"
st.markdown(f'<div class="sg-header"><div><div class="sg-kicker">{k}</div><div class="sg-title">{t}</div></div><div class="{"sg-online" if ready else "sg-offline"}">● {status}</div></div>',unsafe_allow_html=True)

from spectral_figures import spectrum_view

def analyze_file(f,unit):
    r=screen(pd.read_csv(BytesIO(f.getvalue())).to_numpy(float),model,unit)
    g,a,y,ids=model
    scores=(preprocess(r["signal"],g)@a.T)[0]
    order=np.argsort(-scores,kind="stable")[:10]
    ranking=pd.DataFrame({"Rank":np.arange(1,len(order)+1),"Polymer":y[order],"Similarity":scores[order],"Reference ID":ids[order]})
    j=int(np.flatnonzero(ids==r["reference_id"])[0])
    m=~((g>=1500)&(g<1700))
    query=np.full(len(g),np.nan);ref=query.copy()
    query[m]=preprocess(r["signal"],g)[0];ref[m]=a[j]
    row={"file":f.name,"time":datetime.now().isoformat(timespec="seconds"),**{k:v for k,v in r.items() if k!="signal"}}
    return {"row":row,"signal":r["signal"],"grid":g,"query":query,"ref":ref,"ranking":ranking}

def empty_view():
    st.markdown('<div class="sg-empty"><div><strong>SPECTRAL VIEWER</strong>No spectrum loaded</div></div>',unsafe_allow_html=True)

def export_rows(rows,key):
    if rows:
        df=pd.DataFrame(rows)
        st.dataframe(df,hide_index=True,use_container_width=True)
        st.download_button("Export CSV",df.to_csv(index=False).encode(),"seaweedguard_results.csv","text/csv",key=key)

# Built-in examples remain available even without a connected reference bundle.
from demo_examples import load_examples, demo_status
demo_mode=page=="Analyzer" and st.radio("Acquisition source",["Built-in examples","Upload CSV"],horizontal=True,index=0,key="source_mode")=="Built-in examples"
if demo_mode:
    grid,examples=load_examples()
    left,right=st.columns([1,2.6],gap="large")
    with left:
        with st.container(border=True):
            st.markdown("**DEMO ACQUISITION**")
            label=st.selectbox("Sample",list(examples),key="demo_selected",label_visibility="collapsed")
            example=examples[label]
            if st.button("Load example",use_container_width=True):
                st.session_state.demo_loaded=label
                st.session_state.pop("demo_result",None)
            loaded=st.session_state.get("demo_loaded")==label
            if st.button("▶  Analyze spectrum" if ready else "▶  Replay analysis",type="primary",use_container_width=True,disabled=not loaded,key="demo_run"):
                if ready:
                    if not np.allclose(grid,model[0],rtol=0,atol=.00051): st.error("Incompatible model grid");st.stop()
                    rr=screen(np.column_stack([model[0],example["signal"]]),model)
                    result={k:v for k,v in rr.items() if k!="signal"}
                    result["mode"]="Live · rounded example"
                else:
                    result={k:example[k] for k in ("candidate","similarity","margin","accepted","reference_id")}
                    result["status"]=demo_status(result)
                    result["mode"]="Recorded E18 replay"
                st.session_state.demo_result={"label":label,"model_id":model_id,"result":result}
            if st.button("Clear",use_container_width=True,key="demo_clear"):
                st.session_state.pop("demo_loaded",None)
                st.session_state.pop("demo_result",None)
                loaded=False
    with right:
        if loaded:
            current=st.session_state.get("demo_result",{})
            result=current.get("result") if current.get("label")==label and current.get("model_id")==model_id else None
            if result:
                cols=st.columns(3)
                cols[0].metric("POLYMER CANDIDATE",result["candidate"])
                cols[1].metric("SIMILARITY",f'{result["similarity"]:.4f}')
                cols[2].metric("CLASS MARGIN",f'{result["margin"]:.4f}')
                status=result["status"]
                if result["accepted"]: st.success(status)
                elif result["candidate"]=="Other": st.info(status)
                else: st.warning(status)
                st.caption(result["mode"]+" · Known sample: "+example["truth"])
            spectrum_view(grid,[("Measured example",example["signal"])],"Absorbance","demo_"+str(list(examples).index(label)))
            st.caption(example["file"])
            st.download_button("Export example CSV",pd.DataFrame({"wavenumber":grid,"absorbance":example["signal"]}).to_csv(index=False),"example_"+example["file"],"text/csv",key="demo_csv")
            if result:
                st.download_button("Export result",pd.DataFrame([{**result,"file":example["file"],"known_polymer":example["truth"]}]).to_csv(index=False),"demo_result.csv","text/csv",key="demo_result_csv")
                with st.expander("Processing console"):
                    st.code(("LIVE | Frozen engine executed" if ready else "REPLAY | Original E18 recorded scores loaded")+"\\n"+status,language=None)
        else: empty_view()
elif page in ("Analyzer","Batch analysis"):
    batch=page=="Batch analysis"
    left,right=st.columns([1,2.6],gap="large")
    with left:
        with st.container(border=True):
            st.markdown("**ACQUISITION**")
            unit=st.selectbox("Intensity units",["absorbance","percent absorbance","percent transmittance"])
            files=st.file_uploader("Import FTIR CSV" if not batch else "Import FTIR spectra",type=["csv"],accept_multiple_files=batch,key="spectra_"+page)
            files=files if batch else ([files] if files else [])
            st.caption("ATR-FTIR CSV · cm⁻¹")
            run_key=hashlib.sha256(repr((page,model_id,unit,[(f.name,hashlib.sha256(f.getvalue()).hexdigest()) for f in files])).encode()).hexdigest()
            if st.button("▶  Analyze batch" if batch else "▶  Analyze spectrum",type="primary",use_container_width=True,disabled=not (ready and files)):
                results=[];errors=[];logs=[]
                p=st.progress(0,text="Starting analysis")
                for i,f in enumerate(files):
                    try:
                        item=analyze_file(f,unit)
                        results.append(item);st.session_state.history.append(item["row"])
                        logs.append(f"OK | {f.name} | {item['row']['status']}")
                    except Exception as exc:
                        errors.append({"file":f.name,"status":"Invalid input","error":str(exc)})
                        logs.append(f"ERROR | {f.name} | {exc}")
                    p.progress((i+1)/len(files),text=f"Processed {i+1} / {len(files)}")
                st.session_state.runs[page]={"key":run_key,"results":results,"errors":errors,"logs":logs}
            if not ready: st.caption("Model required")
    run=st.session_state.runs.get(page,{})
    current=run if run.get("key")==run_key else {}
    results=current.get("results",[])
    errors=current.get("errors",[])
    with right:
        if not batch:
            if results:
                item=results[0];r=item["row"]
                cols=st.columns(3)
                cols[0].metric("POLYMER CANDIDATE",r["candidate"])
                cols[1].metric("SIMILARITY",f"{r['similarity']:.4f}")
                cols[2].metric("CLASS MARGIN",f"{r['margin']:.4f}")
                if r["accepted"]: st.success("Accepted candidate · confirmation as required")
                elif r["candidate"]=="Other": st.info("Non-target candidate")
                else: st.warning("Tentative candidate · review required")
                a,b=st.tabs(["Measured spectrum","Reference overlay"])
                with a:
                    spectrum_view(item["grid"],[("Measured",item["signal"])],"Absorbance","raw")
                with b:
                    spectrum_view(item["grid"],[("Query",item["query"]),("Nearest reference",item["ref"])],"Normalized first derivative","overlay",mask=True)
                    st.download_button("Export overlay data",pd.DataFrame({"wavenumber":item["grid"],"query":item["query"],"reference":item["ref"]}).to_csv(index=False),"overlay.csv","text/csv")
                st.markdown("**RANKED REFERENCE MATCHES**")
                st.dataframe(item["ranking"],hide_index=True,use_container_width=True,column_config={"Similarity":st.column_config.NumberColumn(format="%.4f")})
                export_rows([r],"single_export")
            else:
                empty_view()
                if errors: st.error(errors[0]["error"])
                else: st.caption("Awaiting acquisition")
        else:
            rows=[x["row"] for x in results]
            cols=st.columns(3)
            cols[0].metric("PROCESSED",len(rows)+len(errors))
            cols[1].metric("ACCEPTED",sum(r["accepted"] for r in rows))
            cols[2].metric("INPUT ERRORS",len(errors))
            if rows or errors: export_rows(rows+errors,"batch_export")
            else: st.caption("Import spectra and start batch analysis.")
        with st.expander("Processing console",expanded=bool(current)):
            st.code("\n".join(current.get("logs",[])) or "IDLE | Awaiting analysis",language=None)
        st.caption("Similarity ≠ probability · isolated spectra only")
elif page=="Reference library":
    if ready:
        g,a,y,ids=model
        df=pd.DataFrame({"Reference ID":ids,"Polymer class":y})
        st.metric("Reference spectra",len(df))
        st.bar_chart(df["Polymer class"].value_counts())
        filter_class=st.selectbox("Polymer class",["All"]+sorted(set(y)))
        st.dataframe(df if filter_class=="All" else df[df["Polymer class"]==filter_class],hide_index=True,use_container_width=True)
    else: st.caption("Model required")
elif page=="Farm monitoring":
    with st.form("farm"):
        c,d=st.columns(2)
        with c: sample=st.text_input("Farm / sample ID");date=st.date_input("Sampling date")
        with d: stage=st.selectbox("Stage",["Cultivation","Harvest","Drying","Transport","Processing"]);location=st.text_input("Site")
        note=st.text_area("Observation");save=st.form_submit_button("Save observation",type="primary")
    if save and sample.strip():
        st.session_state.farm.append({"sample":sample,"date":str(date),"stage":stage,"site":location,"observation":note})
    if st.session_state.farm:
        st.dataframe(pd.DataFrame(st.session_state.farm),hide_index=True,use_container_width=True)
        st.download_button("Export farm log",pd.DataFrame(st.session_state.farm).to_csv(index=False),"farm_log.csv","text/csv")
    st.caption("Session-only records.")
elif page=="History":
    export_rows(st.session_state.history,"history_export")
    if not st.session_state.history: st.caption("No analyses yet")
elif page=="Settings":
    st.table(pd.DataFrame({"Parameter":["Model","References","Grid points","SG window","Polynomial order","Mask (cm⁻¹)","Similarity","Class margin"],"Value":["E18 frozen","459","750","11","2","1500–1700",str(SIM),str(MARGIN)]}))
    st.caption("Locked parameters")
    if ready: st.code(model_id,language=None)
else:
    with st.expander("Quick start"):
        st.write("Analyzer: select a built-in example, load it and run analysis. Without the model bundle, replay displays recorded E18 results; it does not execute new inference. Connect the authorised model for live analysis of uploaded CSVs (header, two numeric columns, wavenumber in cm⁻¹ and intensity). Choose measured intensity units before analysis. Examples are resampled to the E18 grid and rounded to five decimal places. Figure controls affect display/export only. Farm records and history are session-only.")
    st.markdown("**E18 / MicroPlastiX external validation**")
    st.write("DOI: 10.22000/1820 · 3,832 ATR-FTIR spectra.")
    st.markdown("[Demo data source](https://doi.org/10.22000/1820) · [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) · [Attribution](https://github.com/peterDataScientia/SeaweedGuard-/blob/main/assets/DEMO_DATA_LICENSE.md)")
    st.table(pd.DataFrame({"Metric":["PP/PS target accuracy","Accepted target accuracy","Target coverage","Non-target rejection"],"Result":["1027/1203 (85.37%)","767/767 (100%)","767/1203 (63.76%)","2615/2629 (99.47%)"]}))
    st.write("Spectrum-level evaluation. Nylon and PVC were absent from the external dataset. Accepted target accuracy excludes 14 non-target false acceptances. Similarity is not probability. No direct seaweed-tissue, concentration, source-attribution or food-safety validation. The model bundle is supplied separately pending reference-data licence review.")
st.markdown('<div class="sg-foot">SEAWEEDGUARD / 0.2.4 &nbsp;·&nbsp; ATR-FTIR &nbsp;·&nbsp; E18 FROZEN ENGINE</div>',unsafe_allow_html=True)
