# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 01:55:29 2025

@author: Sneha Umbrajkar
"""

import streamlit as st
import pandas as pd
#import plotly.express as px
import numpy as np

st.markdown(
    """
    <style>
    /* Global body (main container) */
    [data-testid="stAppViewContainer"] {
        background-color: #f0f8ff;  /* Light blue */
        color: #FF5733;
        font-family: 'Courier New', monospace;
        font-size: 20px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #222831;
        color: white;
    }

    /* Titles */
    h1, h2, h3 {
        color: #FF5733;
        text-align: center;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 24px;
        color: #0066cc;
        font-weight: bold;
    }
    [data-testid="stMetricDelta"] {
        font-size: 16px;
        color: #008000;
    }

    /* Buttons */
    div.stButton > button {
        background-color: #FF5733;
        color: white;
        border-radius: 10px;
        font-size: 18px;
        padding: 8px 16px;
    }
    div.stButton > button:hover {
        background-color: #e64a19;
        border: 1px solid black;
    }

    /* Input boxes */
    input, select, textarea {
        background-color: #fff8dc;
        border: 2px solid #FF5733;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("🌍 Air Quality Dashboard")

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("SO₂ Level", "24.5 µg/m³", "-2.1%")
col2.metric("NOx Level", "18.3 µg/m³", "+1.8%")
col3.metric("RSPM Level", "45.2 µg/m³", "-0.5%")
col4.metric("TSPM Level", "62.8 µg/m³", "No change")

# Data Entry Form
with st.form("data_entry"):
    date = st.date_input("Date")
    time = st.time_input("Time")
    so2 = st.number_input("SO₂ (µg/m³)")
    nox = st.number_input("NOx (µg/m³)")
    rspm = st.number_input("RSPM (µg/m³)")
    tspm = st.number_input("TSPM (µg/m³)")
    submitted = st.form_submit_button("➕ Add Reading")
    if submitted:
        st.success("Data recorded!")

# Alerts
st.subheader("⚠ Data Quality Alerts")
st.warning("Outlier detected in SO₂ on Jan 14")
st.error("Missing TSPM data on Jan 13")
st.info("Data complete for today")

# Trend Analysis
df = pd.DataFrame({"day": range(100), "SO2": np.random.rand(100)*30})
#fig = px.scatter(df, x="day", y="SO2", title="Trend Analysis")
#st.plotly_chart(fig)

# ML Forecast
st.subheader("🤖 ML Forecast")
st.write("""
- Tomorrow's SO₂: **26.2 µg/m³**  
- Tomorrow's NOx: **19.1 µg/m³**  
- Tomorrow's RSPM: **47.8 µg/m³**  
- Tomorrow's TSPM: **65.3 µg/m³**  
Confidence: 87% | Model: LSTM
""")
