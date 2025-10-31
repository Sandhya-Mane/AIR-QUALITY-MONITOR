import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import tempfile
import numpy as np

# Set page config
st.set_page_config(
    page_title="Air Quality Monitor | Professional Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS styling with clean light theme
st.markdown("""
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

/* Sidebar Headers and Text - Force visibility */
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

/* Sidebar input labels */
[data-testid="stSidebar"] label {
    color: #ffffff !important;
    font-weight: 600 !important;
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

/* All text visibility fixes - More specific targeting */
.stApp p, .stApp span, .stApp div, .stApp label {
    color: #2c3e50 !important;
}

/* Main content text */
.main p, .main span, .main div, .main label {
    color: #2c3e50 !important;
}

/* Sidebar text overrides */
[data-testid="stSidebar"] p, 
[data-testid="stSidebar"] span, 
[data-testid="stSidebar"] div, 
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown {
    color: #2c3e50 !important;
}

/* Tab content text */
[data-baseweb="tab-panel"] p,
[data-baseweb="tab-panel"] span,
[data-baseweb="tab-panel"] div {
    color: #2c3e50 !important;
}

/* Specific text elements */
.stMarkdown p, .stMarkdown span, .stMarkdown div {
    color: #2c3e50 !important;
}

/* Success/info/warning text */
.stSuccess p, .stInfo p, .stWarning p, .stError p {
    color: inherit !important;
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

/* Plotly Charts */
.js-plotly-plot .plotly .modebar {
    background: rgba(248, 249, 250, 0.9);
    border-radius: 5px;
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
""", unsafe_allow_html=True)

# ---------------------------
# Connect to DB
# ---------------------------
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "mini_project_db"
DB_USER = "postgres"
DB_PASS = "root"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# ---------------------------
# Load data
# ---------------------------
@st.cache_data
def load_data():
    query = "SELECT * FROM air_quality_data"
    df = pd.read_sql(query, engine)
    df['datetime'] = pd.to_datetime(df['measurement_datetime'])
    return df

df = load_data()

# ---------------------------
# Outlier Detection Function
# ---------------------------
def detect_outliers(data, column):
    """Detect outliers using IQR method"""
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
    return outliers, lower_bound, upper_bound

# ---------------------------
# PDF Report Generation Function
# ---------------------------
def generate_pdf_report(filtered_df, location, start_date, end_date):
    """Generate comprehensive PDF report with plots and outlier analysis"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#764ba2'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    # Title
    story.append(Paragraph("Air Quality Analysis Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Report metadata
    metadata = [
        ['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        ['Location:', location],
        ['Date Range:', f"{start_date} to {end_date}"],
        ['Total Records:', str(len(filtered_df))]
    ]
    
    meta_table = Table(metadata, colWidths=[2*inch, 4*inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Summary Statistics
    story.append(Paragraph("Summary Statistics", heading_style))
    
    stats_data = [
        ['Pollutant', 'Mean', 'Median', 'Std Dev', 'Min', 'Max'],
        ['SO₂ (μg/m³)', 
         f"{filtered_df['so2_concentration'].mean():.2f}",
         f"{filtered_df['so2_concentration'].median():.2f}",
         f"{filtered_df['so2_concentration'].std():.2f}",
         f"{filtered_df['so2_concentration'].min():.2f}",
         f"{filtered_df['so2_concentration'].max():.2f}"],
        ['NOx (μg/m³)', 
         f"{filtered_df['nox_concentration'].mean():.2f}",
         f"{filtered_df['nox_concentration'].median():.2f}",
         f"{filtered_df['nox_concentration'].std():.2f}",
         f"{filtered_df['nox_concentration'].min():.2f}",
         f"{filtered_df['nox_concentration'].max():.2f}"]
    ]
    
    stats_table = Table(stats_data, colWidths=[1.2*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.9*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9)
    ]))
    story.append(stats_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Create trend plot
    story.append(Paragraph("Pollutant Trends Over Time", heading_style))
    fig = px.line(filtered_df, x='datetime', y=['so2_concentration', 'nox_concentration'],
                  labels={'value': 'Concentration (μg/m³)', 'variable': 'Pollutant'},
                  template='plotly_white',
                  title='Air Quality Trends')
    fig.update_layout(height=400, showlegend=True)
    
    # Save plot as image
    img_bytes = fig.to_image(format="png", width=700, height=400)
    img_buffer = io.BytesIO(img_bytes)
    img = Image(img_buffer, width=6*inch, height=3.4*inch)
    story.append(img)
    story.append(Spacer(1, 0.3*inch))
    
    # Outlier Analysis
    story.append(PageBreak())
    story.append(Paragraph("Outlier Analysis", heading_style))
    
    # SO2 Outliers
    so2_outliers, so2_lower, so2_upper = detect_outliers(filtered_df, 'so2_concentration')
    story.append(Paragraph(f"<b>SO₂ Concentration Outliers:</b>", styles['Normal']))
    story.append(Paragraph(f"Total outliers detected: {len(so2_outliers)}", styles['Normal']))
    story.append(Paragraph(f"Normal range: {so2_lower:.2f} - {so2_upper:.2f} μg/m³", styles['Normal']))
    story.append(Spacer(1, 0.15*inch))
    
    if len(so2_outliers) > 0:
        # Create box plot for SO2
        fig_so2 = go.Figure()
        fig_so2.add_trace(go.Box(y=filtered_df['so2_concentration'], name='SO₂', marker_color='lightblue'))
        fig_so2.update_layout(title='SO₂ Concentration Distribution with Outliers',
                              yaxis_title='Concentration (μg/m³)',
                              height=300)
        img_bytes_so2 = fig_so2.to_image(format="png", width=600, height=300)
        img_buffer_so2 = io.BytesIO(img_bytes_so2)
        img_so2 = Image(img_buffer_so2, width=5*inch, height=2.5*inch)
        story.append(img_so2)
        story.append(Spacer(1, 0.2*inch))
        
        # Top 5 SO2 outliers
        top_so2 = so2_outliers.nlargest(min(5, len(so2_outliers)), 'so2_concentration')[['datetime', 'so2_concentration']]
        outlier_data_so2 = [['Date & Time', 'SO₂ (μg/m³)']]
        for _, row in top_so2.iterrows():
            outlier_data_so2.append([row['datetime'].strftime('%Y-%m-%d %H:%M'), f"{row['so2_concentration']:.2f}"])
        
        outlier_table_so2 = Table(outlier_data_so2, colWidths=[2.5*inch, 2*inch])
        outlier_table_so2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff6b6b')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffe0e0'))
        ]))
        story.append(Paragraph(f"<b>Top {min(5, len(so2_outliers))} SO₂ Outliers:</b>", styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
        story.append(outlier_table_so2)
    else:
        story.append(Paragraph("No SO₂ outliers detected in the selected period.", styles['Normal']))
    
    story.append(Spacer(1, 0.3*inch))
    
    # NOx Outliers
    nox_outliers, nox_lower, nox_upper = detect_outliers(filtered_df, 'nox_concentration')
    story.append(Paragraph(f"<b>NOx Concentration Outliers:</b>", styles['Normal']))
    story.append(Paragraph(f"Total outliers detected: {len(nox_outliers)}", styles['Normal']))
    story.append(Paragraph(f"Normal range: {nox_lower:.2f} - {nox_upper:.2f} μg/m³", styles['Normal']))
    story.append(Spacer(1, 0.15*inch))
    
    if len(nox_outliers) > 0:
        # Create box plot for NOx
        fig_nox = go.Figure()
        fig_nox.add_trace(go.Box(y=filtered_df['nox_concentration'], name='NOx', marker_color='lightgreen'))
        fig_nox.update_layout(title='NOx Concentration Distribution with Outliers',
                              yaxis_title='Concentration (μg/m³)',
                              height=300)
        img_bytes_nox = fig_nox.to_image(format="png", width=600, height=300)
        img_buffer_nox = io.BytesIO(img_bytes_nox)
        img_nox = Image(img_buffer_nox, width=5*inch, height=2.5*inch)
        story.append(img_nox)
        story.append(Spacer(1, 0.2*inch))
        
        # Top 5 NOx outliers
        top_nox = nox_outliers.nlargest(min(5, len(nox_outliers)), 'nox_concentration')[['datetime', 'nox_concentration']]
        outlier_data_nox = [['Date & Time', 'NOx (μg/m³)']]
        for _, row in top_nox.iterrows():
            outlier_data_nox.append([row['datetime'].strftime('%Y-%m-%d %H:%M'), f"{row['nox_concentration']:.2f}"])
        
        outlier_table_nox = Table(outlier_data_nox, colWidths=[2.5*inch, 2*inch])
        outlier_table_nox.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#51cf66')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#d3f9d8'))
        ]))
        story.append(Paragraph(f"<b>Top {min(5, len(nox_outliers))} NOx Outliers:</b>", styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
        story.append(outlier_table_nox)
    else:
        story.append(Paragraph("No NOx outliers detected in the selected period.", styles['Normal']))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

# ---------------------------
# Sidebar Filters
# ---------------------------
st.sidebar.header("Filters")
start_date = st.sidebar.date_input("Start Date", df['datetime'].min())
end_date = st.sidebar.date_input("End Date", df['datetime'].max())
location = st.sidebar.selectbox("Select Location", df['location'].unique())

filtered_df = df[(df['datetime'] >= pd.Timestamp(start_date)) &
                 (df['datetime'] <= pd.Timestamp(end_date)) &
                 (df['location'] == location)]

# ---------------------------
# KPIs
# ---------------------------
st.markdown('<div class="main-header"><h1>Air Quality Dashboard</h1><p class="header-subtitle">Professional Monitoring View</p></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
col1.metric("SO₂ Average", f"{filtered_df['so2_concentration'].mean():.2f} μg/m³")
col2.metric("NOx Average", f"{filtered_df['nox_concentration'].mean():.2f} μg/m³")

# ---------------------------
# Outlier Analysis Section
# ---------------------------
st.markdown('<div class="section-header">🔍 Outlier Detection</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    so2_outliers, so2_lower, so2_upper = detect_outliers(filtered_df, 'so2_concentration')
    st.info(f"**SO₂ Outliers Detected:** {len(so2_outliers)}")
    st.caption(f"Normal Range: {so2_lower:.2f} - {so2_upper:.2f} μg/m³")
    
    if len(so2_outliers) > 0:
        fig_box_so2 = go.Figure()
        fig_box_so2.add_trace(go.Box(y=filtered_df['so2_concentration'], name='SO₂', 
                                     marker_color='lightblue', boxmean='sd'))
        fig_box_so2.update_layout(title='SO₂ Distribution', height=300, showlegend=False)
        st.plotly_chart(fig_box_so2, use_container_width=True)

with col2:
    nox_outliers, nox_lower, nox_upper = detect_outliers(filtered_df, 'nox_concentration')
    st.info(f"**NOx Outliers Detected:** {len(nox_outliers)}")
    st.caption(f"Normal Range: {nox_lower:.2f} - {nox_upper:.2f} μg/m³")
    
    if len(nox_outliers) > 0:
        fig_box_nox = go.Figure()
        fig_box_nox.add_trace(go.Box(y=filtered_df['nox_concentration'], name='NOx', 
                                     marker_color='lightgreen', boxmean='sd'))
        fig_box_nox.update_layout(title='NOx Distribution', height=300, showlegend=False)
        st.plotly_chart(fig_box_nox, use_container_width=True)

# ---------------------------
# Plots
# ---------------------------
st.markdown('<div class="section-header">Pollutant Trends</div>', unsafe_allow_html=True)

fig = px.line(filtered_df, x='datetime', y=['so2_concentration','nox_concentration'],
              labels={'value':'Concentration (μg/m³)','variable':'Pollutant'},
              template='plotly_white')
fig.update_layout(height=500, legend_title_text='Pollutants')
st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Data Table
# ---------------------------
st.markdown('<div class="section-header"> Data Table</div>', unsafe_allow_html=True)
st.dataframe(filtered_df, use_container_width=True)

# ---------------------------
# Download Section
# ---------------------------
st.markdown('<div class="section-header"> Download Options</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV Data",
        data=csv,
        file_name=f'air_quality_{location}_{start_date}_to_{end_date}.csv',
        mime='text/csv'
    )

with col2:
    if st.button("Generate PDF Report"):
        with st.spinner("Generating comprehensive report..."):
            try:
                pdf_buffer = generate_pdf_report(filtered_df, location, start_date, end_date)
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_buffer,
                    file_name=f'air_quality_report_{location}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
                    mime='application/pdf'
                )
                st.success("Report generated successfully!")
            except Exception as e:
                st.error(f"Error generating report: {str(e)}")
