# dataview.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sqlalchemy import create_engine

# Modern CSS styling with clean light theme
DATAVIEW_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global Styles */
.stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    color: #2c3e50 !important;
    font-family: 'Inter', sans-serif;
}

/* Main Container */
.main .block-container {
    padding: 2rem 3rem;
    max-width: 1200px;
}

/* Header Section */
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem 2rem;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    color: white;
}

.main-header h1 {
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    letter-spacing: 2px;
    margin-bottom: 0.5rem !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    color: white !important;
}

.header-subtitle {
    font-size: 1.1rem;
    opacity: 0.9;
    font-style: italic;
    font-weight: 300;
    color: white !important;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%) !important;
    border-right: 3px solid #667eea !important;
}

[data-testid="stSidebar"] .stSelectbox > div > div {
    background-color: white !important;
    border: 2px solid #e9ecef !important;
    border-radius: 10px !important;
    color: #2c3e50 !important;
}

[data-testid="stSidebar"] .stDateInput > div > div > input {
    background-color: white !important;
    border: 2px solid #e9ecef !important;
    border-radius: 10px !important;
    color: #2c3e50 !important;
}

/* Sidebar Headers and Text */
[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
    font-weight: 600 !important;
}

[data-testid="stSidebar"] p, 
[data-testid="stSidebar"] span, 
[data-testid="stSidebar"] label, 
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] .stMarkdown {
    color: #ffffff !important;
    font-weight: 500 !important;
}

[data-testid="stSidebar"] label {
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* Sidebar Buttons */
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    padding: 0.75rem 1rem !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    width: 100% !important;
    margin: 0.5rem 0 !important;
    transition: all 0.3s ease !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    padding: 0.75rem 2rem !important;
    border-radius: 50px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3) !important;
    transition: all 0.3s ease !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
}

/* Metrics */
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border: 1px solid #e9ecef;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    border-left: 5px solid #667eea;
    transition: all 0.3s ease;
}

div[data-testid="metric-container"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
}

div[data-testid="metric-container"] > div {
    font-weight: 600;
    color: #2c3e50;
}

div[data-testid="metric-container"] [data-testid="metric-value"] {
    color: #667eea !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
}

/* Cards */
.dashboard-card {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    margin: 1.5rem 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    border: 1px solid #e9ecef;
}

/* Main content text */
.main p, .main span, .main div, .main label {
    color: #2c3e50 !important;
}

/* Section headers */
.section-header {
    color: #667eea !important;
    font-size: 1.5rem !important;
    font-weight: 600 !important;
    margin-bottom: 1.5rem !important;
    padding-bottom: 0.5rem !important;
    border-bottom: 3px solid #667eea !important;
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
}

/* Success/Error Messages */
.stSuccess {
    background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
    border: 1px solid #c3e6cb;
    border-radius: 10px;
    color: #155724;
}

.stError {
    background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
    border: 1px solid #f5c6cb;
    border-radius: 10px;
    color: #721c24;
}

.stWarning {
    background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
    border: 1px solid #ffeaa7;
    border-radius: 10px;
    color: #856404;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 5px;
}

.stTabs [data-baseweb="tab"] {
    height: 50px;
    padding: 10px 20px;
    background-color: transparent;
    border-radius: 10px;
    color: #6c757d;
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
}

/* Dataframe */
.stDataFrame {
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
}

/* Download Buttons */
.stDownloadButton > button {
    background: linear-gradient(135deg, #28a745 0%, #20c997 100%) !important;
    color: white !important;
    border: none !important;
    padding: 0.75rem 1.5rem !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
}

.stDownloadButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 5px 15px rgba(40, 167, 69, 0.3) !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background-color: white;
    border: 2px solid #e9ecef;
    border-radius: 10px;
}

/* Input Fields */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stDateInput > div > div > input {
    background-color: white;
    border: 2px solid #e9ecef;
    border-radius: 10px;
    color: #2c3e50;
}
</style>
"""

# Database connection
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "mini_project_db"
DB_USER = "postgres"
DB_PASS = "root"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Load data
@st.cache_data
def load_data():
    query = "SELECT * FROM air_quality_data"
    df = pd.read_sql(query, engine)
    df['datetime'] = pd.to_datetime(df['measurement_datetime'])
    return df

def dataview_page():
    st.markdown(DATAVIEW_CSS, unsafe_allow_html=True)
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("### 🌿 Navigation")
        st.markdown("---")
        
        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state.current_page = 'dashboard'
            st.experimental_rerun()
        
        if st.button("📈 Data View", use_container_width=True, type="primary"):
            st.session_state.current_page = 'dataview'
            st.experimental_rerun()
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            # Clear session state
            for key in ['logged_in', 'user_name', 'user_email', 'user_role', 'current_page']:
                if key in st.session_state:
                    del st.session_state[key]
            st.experimental_rerun()
        
        st.markdown("---")
        st.markdown(f"**User:** {st.session_state.get('user_name', 'Guest')}")
        st.markdown(f"**Role:** {st.session_state.get('user_role', 'N/A')}")
    
    # Load data
    df = load_data()
    
    # Data Filters Section in Sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔍 Filters")
    start_date = st.sidebar.date_input("Start Date", df['datetime'].min())
    end_date = st.sidebar.date_input("End Date", df['datetime'].max())
    location = st.sidebar.selectbox("Select Location", df['location'].unique())
    
    # Filter data
    filtered_df = df[(df['datetime'] >= pd.Timestamp(start_date)) &
                     (df['datetime'] <= pd.Timestamp(end_date)) &
                     (df['location'] == location)]
    
    # Main Content
    st.markdown('<div class="main-header"><h1>Air Quality Dashboard</h1><p class="header-subtitle">Professional Monitoring View</p></div>', unsafe_allow_html=True)
    
    # KPIs
    col1, col2 = st.columns(2)
    col1.metric("SO₂ Average", f"{filtered_df['so2_concentration'].mean():.2f} μg/m³")
    col2.metric("NOx Average", f"{filtered_df['nox_concentration'].mean():.2f} μg/m³")
    
    # Plots
    st.markdown('<div class="section-header">Pollutant Trends</div>', unsafe_allow_html=True)
    
    fig = px.line(filtered_df, x='datetime', y=['so2_concentration','nox_concentration'],
                  labels={'value':'Concentration (μg/m³)','variable':'Pollutant'},
                  template='plotly_white')
    fig.update_layout(height=500, legend_title_text='Pollutants')
    st.plotly_chart(fig, use_container_width=True)
    
    # Data Table
    st.markdown('<div class="section-header">Data Table</div>', unsafe_allow_html=True)
    st.dataframe(filtered_df[1:])
    
    # Download
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name='air_quality_filtered.csv',
        mime='text/csv'
    )