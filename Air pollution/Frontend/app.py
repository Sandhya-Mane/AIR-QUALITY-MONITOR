# -*- coding: utf-8 -*-
"""
Created on Fri Oct 31 00:54:26 2025

@author: Sneha Umbrajkar
"""

# app.py - Main Application Controller
import streamlit as st

# Page configuration MUST be first
st.set_page_config(
    page_title="Air Quality Monitor | Professional Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import pages
from login_ui import login_page
from dataview import dataview_page
from dashboard import admin_dashboard

def main():
    """Main application controller"""
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'dataview'  # Default landing page after login
    
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = 'login'
    
    # Routing logic
    if not st.session_state.logged_in:
        # User not logged in - show login page
        login_page()
    else:
        # User logged in - route to appropriate page
        if st.session_state.current_page == 'dataview':
            dataview_page()
        elif st.session_state.current_page == 'dashboard':
            admin_dashboard()
        else:
            # Default to dataview if unknown page
            st.session_state.current_page = 'dataview'
            dataview_page()

if __name__ == "__main__":
    main()