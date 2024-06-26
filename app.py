#Import all related libraries
import streamlit as st
import pandas as pd

# df = pd.read_excel('TA_Tracking_Module_v1.xlsm', 'Position')

#Page setup using streamlit
st.set_page_config(page_title="TA Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide"
)
#----Main page ------
st.title(":bar_chart: TA Dashboard")
st.subheader("Annual Positon and Application Tracking")

st.markdown("##")


lcol, midcol, rcol = st.columns(3)

st.markdown("###")

