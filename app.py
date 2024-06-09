#Import all related libraries
import pandas as pd
import streamlit as st
import plotly as px
from PIL import Image
import calendar as cal
from datetime import date


# @st.cache_resource
#Get data from excel file into dataframe
def get_xlData():
    df = pd.read_excel("TA_Tracking_Module_v1.xlsm", "Position")
    return df

df = get_xlData()

#Add approval month into dataframe
df["Appr_Date"] = pd.to_datetime(df["Appr_Date"]).dt.normalize()
df["Month"] = df["Appr_Date"].dt.month

#Page setup using streamlit
st.set_page_config(page_title="TA Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide"
)
#----Main page ------
st.title(":bar_chart: TA Dashboard")
st.subheader("Annual Positon and Application Tracking")

#----Sidebar--------
st.sidebar.header("Please filter here!")
stat = st.sidebar.multiselect(
    "Select Status:",
    options=df["Post_Status"].unique(),
    default=df["Post_Status"].unique()
)

bu = st.sidebar.multiselect(
    "Select BU:",
    options=df["BU"].unique(),
    default=df["BU"].unique()
)

dept = st.sidebar.multiselect(
    "Select Department:",
    options=df["Department"].unique(),
    default=df["Department"].unique()
)

#Query dataframe based on filter selected
df_select = df.query(
    "Post_Status == @stat & BU == @bu & Department == @dept"
)

st.markdown("##")

#Label card
total_post = df_select["PostID"].count()
total_open_post = df_select["Post_Status"].isnull().sum()
total_close_post = df_select[df_select["Post_Status"]=="Cancelled"].count()["Post_Status"]

lcol, midcol, rcol = st.columns(3)
with lcol:
    st.subheader("Total Positions")
    st.subheader(f"{total_post}")

with midcol:
    st.subheader("#Open Positions")
    st.subheader(total_open_post)

with rcol:
    st.subheader("#Closed Positions")
    st.subheader(f"{total_close_post}")

st.markdown("###")

#Prepare data for charts count of position by BU
post_by_bu = (df_select.groupby(by=["BU"])
              .agg({'PostID':'count'})
              .sort_values('PostID')
              .rename(columns={'PostID':'Position Count'})
)

#Create count of position by BU chart 
chart_by_bu = px.bar(
    post_by_bu,
    y = "Position Count",
    x = post_by_bu.index,
    orientation="v",
    labels="PostID",
    title="<b>Count of Position by BU<B>",
    color_discrete_sequence=["#008388"] * len(post_by_bu),
    template="plotly_white",
    text_auto=True,
)

chart_by_bu.update_traces(textposition='outside')

#Exstract approve date dataframe
df_appr_date = df_select.loc[:,'Appr_Date':'Appr_Date']
df_appr_date['Year'] = df_appr_date['Appr_Date'].dt.year
df_appr_date['Month'] = df_appr_date['Appr_Date'].dt.month
# df_appr_date['Month'] = df_appr_date['Month'].apply(lambda x: cal.month_abbr[x])
df_appr_date['Month'] = df_appr_date['Year'].map(str) + '-' + df_appr_date['Month'].map(str)
df_appr_date['Post by Month'] = 'Position'

#Prepare data for count of new position by month
post_by_month = (df_appr_date.groupby(by=['Month'])
                 .agg({'Year':'count'})
                 .rename(columns={'Year':'Position Count'})
)

#Create chart for count of position by month
chart_by_month = px.bar(
    post_by_month,
    x = post_by_month.index,
    y = "Position Count",
    orientation="v",
    title="<b>Count of Position by Month<B>",
    color_discrete_sequence=["#2596be"] * len(post_by_month),
    template="plotly_white",
    text_auto=True,
)

chart_by_month.update_traces(textposition='outside')

#Prepare chart layout
col1, col2 = st.columns(2)

#Uplaod chart into steamlit
with col1:
    st.plotly_chart(chart_by_bu)

with col2:
    st.plotly_chart(chart_by_month)

st.markdown("---")

#Upload filtered dataframe into streamlit
st.dataframe(df_select)

df_out = pd.crosstab(pd.PeriodIndex(df_appr_date['Appr_Date'], freq='M'),df_appr_date['Post by Month'])
fig = px.bar(
    df_out,
    x='Position',
    y=df_out.index,
)


