# -*- coding: utf-8 -*-
"""
Created on Thu Sep 18 16:42:25 2025

@author: Sneha Umbrajkar
"""

import streamlit as st

st.markdown(
    """
    <style>
    /* Change background color */
    .stApp {
        font-family: "Comic Sans MS", cursive, sans-serif;
        background-color: #f5f7fa;
    }

    /* Change sidebar color */
    [data-testid="stSidebar"] {
        background-color: #2e3b4e;
        color: white;
    }

    /* Customize headers */
    h1 {
        color: #ff5733;
        font-family: 'Courier New', monospace;
    }

    /* Style buttons */
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("Demo file")
