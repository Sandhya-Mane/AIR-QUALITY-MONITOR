# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 14:48:33 2025

@author: Sneha Umbrajkar
"""

LOGIN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

.stApp {
    background: linear-gradient(135deg, #e0e7ff, #f3f4f6);
}

h1 { color: #1f2937 !important; font-weight: 700; } 
p { color: #4b5563 !important; font-size: 0.95rem; }

.stTextInput > div > div > input {
    color: #1f2937 !important; 
    border-radius: 10px !important;
    padding: 14px 14px !important;
    border: 1.5px solid #e5e7eb !important;
    background: #f9fafb !important;
}

div.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 14px 0 !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}

div.stButton > button:hover {
    background: linear-gradient(135deg, #764ba2, #667eea) !important;
    color: #ffffff !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 18px rgba(102, 126, 234, 0.4) !important;
}

#MainMenu, footer, header { visibility: hidden; }
</style>
"""

DASHBOARD_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    color: #2c3e50 !important;
}

.stApp {
    background: #f5f7fa !important; 
    color: #2c3e50 !important;
    font-family: 'Inter', sans-serif;
}

h1, h2, h3, h4, h5, h6, p, span, div, label {
    color: #2c3e50 !important;
}

.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
}

.main-header h1 {
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    color: white !important;
    margin-bottom: 0.5rem !important;
}

.header-subtitle {
    font-size: 1.1rem;
    color: white !important;
}

.user-info {
    color: white !important;
    font-size: 0.9rem;
    margin-top: 1rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #e8f4fd 0%, #f0f8ff 30%, #f5f7ff 100%) !important;
    border-right: 3px solid #667eea !important;
}

[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #2c3e50 !important;
    font-weight: 600 !important;
}

div[data-testid="metric-container"] {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border: 1px solid #e9ecef;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    border-left: 5px solid #667eea;
}

.dashboard-card {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    margin: 1.5rem 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    font-weight: 600 !important;
}

.stTextInput > div > div > input {
    color: #2c3e50 !important;
    background: white !important;
}

.stTimeInput > div > div > input {
    color: #2c3e50 !important;
    background: white !important;
}

input[type="time"] {
    color: #2c3e50 !important;
    background: white !important;
}

.stSelectbox > div > div {
    background: white !important;
    color: #2c3e50 !important;
}

.stSelectbox > div > div > div {
    color: #2c3e50 !important;
}

.stSelectbox > div > div > div > div {
    color: #2c3e50 !important;
}

.stDateInput > div > div > input {
    color: #2c3e50 !important;
    background: white !important;
}

input, textarea {
    color: #2c3e50 !important;
    background: white !important;
}

/* Fix for dropdown options visibility */
section[data-testid="stSidebar"] div[data-baseweb="select"] div {
    color: #2c3e50 !important;
    background-color: white !important;
}

div[data-baseweb="select"] div {
    color: #2c3e50 !important;
    background-color: white !important;
}

div[data-baseweb="popover"] div {
    color: #2c3e50 !important;
    background-color: white !important;
}

div[data-baseweb="menu"] li {
    color: #2c3e50 !important;
    background-color: white !important;
}

div[data-baseweb="menu"] li:hover {
    background-color: #f0f0f0 !important;
    color: #2c3e50 !important;
}

/* Fix for all dropdown elements */
[data-baseweb="select"] > div {
    color: #2c3e50 !important;
    background: white !important;
}

[data-baseweb="popover"] {
    background: white !important;
    color: #2c3e50 !important;
}

[data-baseweb="menu"] {
    background: white !important;
    color: #2c3e50 !important;
}

[data-baseweb="menu"] li {
    background: white !important;
    color: #2c3e50 !important;
}

[data-baseweb="menu"] li:hover {
    background: #f0f0f0 !important;
    color: #2c3e50 !important;
}

[data-baseweb="tab-list"] * {
    color: #2c3e50 !important;
}

.stNumberInput > div > div > input {
    color: #2c3e50 !important;
    background: white !important;
}

#MainMenu, footer, header { visibility: hidden; }
</style>
"""