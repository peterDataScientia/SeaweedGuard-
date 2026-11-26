"""Interactive FTIR viewer plus exact Figentra publication rendering."""
from io import BytesIO
import numpy as np
import plotly.graph_objects as go
import streamlit as st
from figentra import style_context, new_figure, style_axes, legend_bold
from spectral_units import display_signal, UNITS
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

@st.cache_data(show_spinner=False)
def publication_bytes(x, series, ylabel, mask, limits, yrange, line_width, palette, legend, fmt):
    with style_context():
        fig,ax=new_figure()
        try:
            for i,(label,y) in enumerate(series):
                ax.plot(x,y,color=palette[i%len(palette)],lw=line_width,label=label,ls="-" if i==0 else "--")
            if mask: ax.axvspan(1500,1700,color="#d0d0d0",alpha=.30,zorder=0)
            style_axes(ax,xlabel="Wavenumber [cm⁻¹]",ylabel=ylabel)
            ax.set_xlim(limits[1],limits[0])
            if yrange: ax.set_ylim(*yrange)
            ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
            ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
            if legend and len(series)>1: legend_bold(ax,loc="best")
            fig.subplots_adjust(left=.23,right=.96,bottom=.19,top=.96)
            buf=BytesIO()
            fig.savefig(buf,format=fmt,dpi=600,facecolor="white")
            return buf.getvalue()
        finally: plt.close(fig)

def spectrum_view(x, series, ylabel, key, mask=False, tools=None):
    x=np.asarray(x,dtype=float)
    series=[(str(n),np.asarray(v,dtype=float)) for n,v in series]
    controls, exports = st.columns([1,1]) if tools is None else (tools,tools)
    unit_tag=""
    if ylabel=="Absorbance":
        selected=controls.selectbox("Display units",UNITS,key=key+"_display_unit")
        try:
            series=[(n,display_signal(v,selected)) for n,v in series]
        except FloatingPointError:
            st.error("Intensity conversion exceeds numeric range.");return
        ylabel={"Absorbance":"Absorbance","% Absorbance":"Absorbance [%]","% Transmittance":"Transmittance [%]"}[selected]
        unit_tag="_"+str(UNITS.index(selected))
    with controls.popover("Figure controls",use_container_width=True):
        a,b,c=st.columns(3)
        style=a.selectbox("Style",["Digital","Publication"],key=key+"_style")
        lw=b.slider("Line width",1.,4.,2.,.25,key=key+"_lw")
        height=c.slider("Viewer height",300,800,450,25,key=key+"_height")
        a,b=st.columns(2)
        legend=a.checkbox("Show legend",value=len(series)>1,key=key+"_legend")
        autoscale=b.checkbox("Auto Y scale",value=True,key=key+"_auto")
        lo,hi=float(x.min()),float(x.max())
        limits=st.slider("Wavenumber range [cm⁻¹]",lo,hi,(lo,hi),step=1.,key=key+"_range")
        if limits[1]<=limits[0]:
            st.caption("Choose a nonzero spectral interval.")
            limits=(lo,hi)
        visible=st.multiselect("Visible traces",[n for n,_ in series],default=[n for n,_ in series],key=key+"_traces")
        show_mask=st.checkbox("Show excluded region",value=True,key=key+"_mask") if mask else False
    series=[(n,v) for n,v in series if n in visible]
    if not series:
        st.info("Select at least one spectral trace.");return
    yrange=None
    if not autoscale:
        vals=np.concatenate([v[np.isfinite(v)] for _,v in series])
        if vals.size:
            low,high=float(vals.min()),float(vals.max())
            if high<=low: high=low+max(abs(low)*.05,.001)
            pad=(high-low)*.05
            yrange=st.slider("Y-axis range",low-pad,high+pad,(low-pad,high+pad),key=key+"_yrange"+unit_tag,format="%.5f")
    pub=style=="Publication"
    palette=("#111111","#C43C35") if pub else ("#23D5C6","#FFB454")
    bg="#FFFFFF" if pub else "#0C1A29"
    fg="#000000" if pub else "#E7F2FA"
    fig=go.Figure()
    for i,(label,y) in enumerate(series):
        fig.add_trace(go.Scatter(x=x,y=y,name=label,mode="lines",line=dict(color=palette[i%len(palette)],width=lw*(1.333 if pub else 1),dash="solid" if i==0 else "dash"),connectgaps=False,hovertemplate="%{x:.2f} cm⁻¹<br>%{y:.6g}<extra>%{fullData.name}</extra>"))
    if show_mask: fig.add_vrect(x0=1500,x1=1700,fillcolor="#9DA9B3",opacity=.20,line_width=0,layer="below")
    axis=dict(showline=True,linecolor=fg,linewidth=2.67 if pub else 1.3,ticks="outside",ticklen=8 if pub else 5,tickwidth=2.67 if pub else 1,showgrid=False,zeroline=False,tickfont=dict(size=16 if pub else 13,family="DejaVu Sans",color=fg,weight=700 if pub else 400),nticks=6)
    fig.update_layout(template="none",paper_bgcolor=bg,plot_bgcolor=bg,height=height,margin=dict(l=76,r=18,t=38 if legend else 16,b=62),font=dict(family="DejaVu Sans",color=fg,size=16 if pub else 13),showlegend=legend,legend=dict(orientation="h",y=1.02,x=0,font=dict(size=14.67 if pub else 13,weight=700 if pub else 400,color=fg,family="DejaVu Sans")),xaxis=dict(**axis,title=dict(text="Wavenumber [cm⁻¹]",font=dict(size=20 if pub else 15,weight=700,color=fg,family="DejaVu Sans")),range=[limits[1],limits[0]]),yaxis=dict(**axis,title=dict(text=ylabel,font=dict(size=20 if pub else 15,weight=700,color=fg,family="DejaVu Sans")),range=list(yrange) if yrange else None,autorange=yrange is None),hovermode="x unified",dragmode="zoom")
    st.plotly_chart(fig,use_container_width=True,theme=None,config={"displaylogo":False,"scrollZoom":True,"responsive":True,"toImageButtonOptions":{"format":"png","filename":"seaweedguard_view","scale":2}},key=key+"_chart"+unit_tag)
    with exports.popover("Export figure",use_container_width=True):
        st.caption("600 DPI · Figentra · selected axis range")
        fmt=st.selectbox("Format",["png","svg","pdf"],key=key+"_format")
        if st.button("Prepare publication figure",key=key+"_prepare"):
            signature=repr((limits,yrange,lw,legend,show_mask,fmt,[(n,v.tobytes()) for n,v in series],x.tobytes(),ylabel))
            st.session_state[key+"_export"]=(signature,publication_bytes(x,series,ylabel,show_mask,limits,yrange,lw,("#111111","#C43C35"),legend,fmt))
        signature=repr((limits,yrange,lw,legend,show_mask,fmt,[(n,v.tobytes()) for n,v in series],x.tobytes(),ylabel))
        saved=st.session_state.get(key+"_export")
        if saved and saved[0]==signature:
            st.download_button("Download "+fmt.upper(),saved[1],"seaweedguard_"+key+"."+fmt,{"png":"image/png","svg":"image/svg+xml","pdf":"application/pdf"}[fmt],key=key+"_download")
