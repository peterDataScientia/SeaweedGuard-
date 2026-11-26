import streamlit as st
import numpy as np
import pandas as pd
from pathlib import Path
from screening import screen
st.set_page_config(page_title='SeaweedGuard',page_icon='🌊')
st.title('SeaweedGuard — spectral screening prototype')
st.warning('Research demonstration only. PP/PVC reference; other materials may be misidentified. Not validated for seaweed, food safety or source attribution.')
ref=Path(__file__).parent/'results/reference.npz'
if not ref.exists(): st.error('Generate reference.npz using benchmark.py first.');st.stop()
z=np.load(ref);st.write('Upload two numeric columns: wavenumber (cm⁻¹) and percent absorbance, with header.')
f=st.file_uploader('Spectrum CSV',type=['csv'])
if f:
    try:
        res=screen(pd.read_csv(f).to_numpy(dtype=float),z)
        st.metric('Nearest reference correlation',f"{res['similarity']:.4f}")
        st.write('Screening result:',res['candidate'] if res['accepted'] else 'Refer for expert review')
        st.caption('Similarity is not a probability; other materials may be misidentified.')
        st.line_chart(pd.DataFrame({'signal':res['signal']},index=z['wavenumber']))
    except Exception as e: st.error('Invalid or incompatible spectrum: '+str(e))
st.subheader('Farm monitoring log (session only)')
with st.form('monitor'):
    site=st.text_input('Farm / sample ID');stage=st.selectbox('Stage',['Cultivation','Harvest','Drying','Transport','Processing']);note=st.text_area('Observed possible contamination source / intervention');submit=st.form_submit_button('Record observation')
if 'records' not in st.session_state:st.session_state.records=[]
if submit and site.strip():st.session_state.records.append(dict(sample=site,stage=stage,observation=note))
if st.session_state.records:
    table=pd.DataFrame(st.session_state.records);st.dataframe(table);st.download_button('Export observation log',table.to_csv(index=False),'farm_log.csv','text/csv')
st.caption('Observations are hypotheses; source attribution and mitigation efficacy require sampling controls.')
