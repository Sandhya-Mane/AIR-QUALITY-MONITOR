# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 14:48:14 2025

@author: Sneha Umbrajkar
"""
import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
import hashlib

# Database configuration
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "mini_project_db"
DB_USER = "postgres"
DB_PASS = "root"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Locations constant
LOCATIONS = ["Mumbai Central", "Andheri", "Bandra", "Worli", "Thane"]

# CSS Styling
DASHBOARD_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

.stApp {
    background: linear-gradient(135deg, #e0e7ff, #f3f4f6);
}

.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
}

.main-header h1 {
    color: white !important;
    font-size: 2.5rem;
    margin: 0;
    font-weight: 700;
}

.header-subtitle {
    color: rgba(255, 255, 255, 0.9);
    font-size: 1.1rem;
    margin-top: 0.5rem;
}

.user-info {
    color: rgba(255, 255, 255, 0.95);
    font-size: 1rem;
    margin-top: 0.5rem;
}

div.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 0.5rem 1rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
}

.stMetric {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>
"""

# Database helper functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load all users from database"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, name, email, role FROM users"))
            users = {}
            for row in result:
                users[row[2]] = {  # Use email as key
                    'id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'role': row[3],
                    'status': 'Active'  # Default status
                }
            return users
    except Exception as e:
        st.error(f"Error loading users: {e}")
        return {}

def save_user(email, password, name, role='user'):
    """Save a new user to database"""
    hashed_pwd = hash_password(password)
    try:
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO users (name, email, password, role) VALUES (:name, :email, :password, :role)"),
                {"name": name, "email": email, "password": hashed_pwd, "role": role}
            )
        return True
    except Exception as e:
        st.error(f"Error saving user: {e}")
        return False

def update_user_role(email, new_role):
    """Update user role in database"""
    try:
        with engine.begin() as conn:
            conn.execute(
                text("UPDATE users SET role = :role WHERE email = :email"),
                {"role": new_role, "email": email}
            )
        return True
    except Exception as e:
        st.error(f"Error updating user role: {e}")
        return False

def delete_user(email):
    """Delete user from database"""
    try:
        with engine.begin() as conn:
            conn.execute(
                text("DELETE FROM users WHERE email = :email"),
                {"email": email}
            )
        return True
    except Exception as e:
        st.error(f"Error deleting user: {e}")
        return False

def logout():
    """Clear session state and logout"""
    for key in ['logged_in', 'user_name', 'user_email', 'user_role', 'auth_mode']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

def generate_air_quality_data(start_date, end_date, location):
    """Generate synthetic air quality data"""
    date_range = pd.date_range(start=start_date, end=end_date, freq='H')
    np.random.seed(42)

    data = []
    for dt in date_range:
        hour = dt.hour
        month = dt.month

        daily_factor = 1 + 0.3 * np.sin((hour - 6) * np.pi / 12) if 6 <= hour <= 20 else 0.7
        seasonal_factor = 1.5 if month in [11, 12, 1, 2] else 1.0
        base_pollution = daily_factor * seasonal_factor

        so2 = max(5, np.random.normal(30 * base_pollution, 15))
        nox = max(10, np.random.normal(60 * base_pollution, 25))
        rspm = max(20, np.random.normal(100 * base_pollution, 35))
        tspm = max(40, np.random.normal(180 * base_pollution, 50))

        max_pollutant = max(so2/80, nox/180, rspm/150, tspm/300)
        status = "Poor" if max_pollutant > 1.5 else "Moderate" if max_pollutant > 1.0 else "Good"

        data.append({
            'DateTime': dt,
            'Date': dt.date(),
            'SO₂ (μg/m³)': round(so2, 1),
            'NOₓ (μg/m³)': round(nox, 1),
            'RSPM (μg/m³)': round(rspm, 1),
            'TSPM (μg/m³)': round(tspm, 1),
            'AQI_Status': status,
            'Location': location
        })

    return pd.DataFrame(data)

def create_time_series_plot(df):
    """Create time series plot for air quality data"""
    fig = go.Figure()
    colors = ['#667eea', '#764ba2', '#f39c12', '#e74c3c']
    pollutants = ['SO₂ (μg/m³)', 'NOₓ (μg/m³)', 'RSPM (μg/m³)', 'TSPM (μg/m³)']
    names = ['SO₂', 'NOₓ', 'RSPM', 'TSPM']

    for i, pollutant in enumerate(pollutants):
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df[pollutant],
            name=names[i],
            line=dict(color=colors[i], width=3, shape='spline'),
            mode='lines',
            hovertemplate='<b>' + names[i] + '</b><br>%{x|%d %b %Y %H:%M}<br>%{y:.1f} μg/m³<extra></extra>'
        ))

    fig.update_layout(
        title=dict(
            text="Air Quality Trends Over Time",
            font=dict(size=22, color='black'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title="Date & Time",
            title_font=dict(size=14, color='black'),
            tickfont=dict(size=12, color='black'),
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        ),
        yaxis=dict(
            title="Concentration (μg/m³)",
            title_font=dict(size=14, color='black'),
            tickfont=dict(size=12, color='black'),
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black', size=12),
        height=600,
        hovermode='x unified',
        legend=dict(
            bgcolor='rgba(255,255,255,0.95)',
            bordercolor='black',
            borderwidth=1,
            font=dict(color='black', size=11)
        ),
        margin=dict(l=100, r=60, t=100, b=100)
    )
    return fig

def readings_page():
    """Placeholder for readings page"""
    st.markdown("""
    <div class="main-header">
        <h1>SENSOR READINGS</h1>
        <div class="header-subtitle">Real-time monitoring data</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("Sensor readings functionality will be implemented here.")
    st.write("This section will display real-time sensor data from monitoring stations.")

def admin_dashboard():
    st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("## Admin Panel")
        page = st.radio("Navigation", ["Dashboard", "Data View", "Readings", "User Management", "Settings"], label_visibility="collapsed")
        st.markdown("---")
        if st.button("Logout", key="logout_admin_btn", use_container_width=True):
            logout()

    if page == "Dashboard":
        st.markdown(f"""
        <div class="main-header">
            <h1>ADMIN DASHBOARD</h1>
            <div class="header-subtitle">System Overview</div>
            <div class="user-info">Welcome, {st.session_state.user_name}</div>
        </div>
        """, unsafe_allow_html=True)

        users_db = load_users()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Users", len(users_db))
        with col2:
            admin_count = sum(1 for u in users_db.values() if u['role'] == 'admin')
            st.metric("Admins", admin_count)
        with col3:
            user_count = sum(1 for u in users_db.values() if u['role'] == 'user')
            st.metric("Regular Users", user_count)

        st.markdown("---")
        st.subheader("Recent Users")
        recent_users = list(users_db.values())[-5:]
        for user in recent_users:
            st.write(f"👤 **{user['name']}** ({user['role']}) - {user['email']}")

    elif page == "Data View":
        st.markdown(f"""
        <div class="main-header">
            <h1>AIR QUALITY MONITOR</h1>
            <div class="header-subtitle">Data Analytics Dashboard</div>
            <div class="user-info">
                Welcome, {st.session_state.user_name}
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.sidebar:
            st.markdown("### Control Panel")
            start_date = st.date_input("Start Date", value=datetime(2024, 1, 1), key="admin_start_date")
            end_date = st.date_input("End Date", value=datetime(2024, 1, 7), key="admin_end_date")
            selected_location = st.selectbox("Monitoring Station", options=LOCATIONS, index=0, key="admin_location")
            max_records = st.selectbox("Data Points Limit", options=[500, 1000, 2000, 5000, "All"], index=1, key="admin_records")
            apply_filters = st.button("Analyze Data", type="primary", use_container_width=True, key="admin_analyze")

        if apply_filters:
            if start_date > end_date:
                st.error("Invalid Date Range!")
                return

            with st.spinner("Fetching data..."):
                df = generate_air_quality_data(start_date, end_date, selected_location)
                if max_records != "All" and len(df) > max_records:
                    df = df.sample(n=max_records, random_state=42).sort_values('DateTime')

            st.success(f"Data Retrieved: {len(df):,} records loaded")

            col1, col2, col3, col4 = st.columns(4)
            status_counts = df['AQI_Status'].value_counts()

            with col1:
                st.metric("Total Data Points", f"{len(df):,}")
            with col2:
                st.metric("Good Quality", status_counts.get('Good', 0))
            with col3:
                st.metric("Moderate Quality", status_counts.get('Moderate', 0))
            with col4:
                st.metric("Poor Quality", status_counts.get('Poor', 0))

            tab1, tab2, tab3 = st.tabs(["Trends", "Distribution", "Data"])

            with tab1:
                fig = create_time_series_plot(df)
                st.plotly_chart(fig, use_container_width=True, key="admin_chart")

            with tab2:
                st.dataframe(df[['SO₂ (μg/m³)', 'NOₓ (μg/m³)', 'RSPM (μg/m³)', 'TSPM (μg/m³)']].describe(), use_container_width=True)

            with tab3:
                st.dataframe(df, use_container_width=True)
                csv_data = df.to_csv(index=False).encode('utf-8')
                st.download_button("Download Data", csv_data, f"air_quality_{start_date}_{end_date}.csv", "text/csv")
        else:
            st.info("Configure parameters in the sidebar and click 'Analyze Data' to begin")

    elif page == "User Management":
        st.markdown(f"""
        <div class="main-header">
            <h1>USER MANAGEMENT</h1>
            <div class="header-subtitle">Manage system users and permissions</div>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["View Users", "Add New User"])

        with tab1:
            users_db = load_users()
            col1, col2 = st.columns([3, 1])

            with col1:
                search = st.text_input("Search users...")
            with col2:
                role_filter = st.selectbox("Filter by Role", ["All", "admin", "user"])

            users_list = list(users_db.values())

            if search:
                users_list = [u for u in users_list if search.lower() in u['name'].lower() or search.lower() in u['email'].lower()]

            if role_filter != "All":
                users_list = [u for u in users_list if u['role'] == role_filter]

            for user in users_list:
                col1, col2, col3, col4, col5 = st.columns([2, 2, 1.5, 1, 1.5])

                with col1:
                    st.write(f"**{user['name']}**")
                    st.caption(user['email'])

                with col2:
                    st.write(user['status'])

                with col3:
                    st.write(f"**Role:** {user['role']}")

                with col4:
                    new_role = st.selectbox("Change Role", ["admin", "user"], key=f"role_{user['email']}")
                    if st.button("Update", key=f"update_{user['email']}", use_container_width=True):
                        update_user_role(user['email'], new_role)
                        st.success("Role updated!")
                        st.rerun()

                with col5:
                    if user['email'] != st.session_state.user_email and user['email'] != 'admin@airquality.com':
                        if st.button("Delete", key=f"delete_{user['email']}", use_container_width=True):
                            delete_user(user['email'])
                            st.success("User deleted!")
                            st.rerun()

                st.divider()

        with tab2:
            st.subheader("Add New User")
            with st.form("add_user_form"):
                new_name = st.text_input("Full Name")
                new_email = st.text_input("Email")
                new_password = st.text_input("Password", type="password")
                new_role = st.selectbox("Role", ["user", "admin"])
                submit = st.form_submit_button("Add User", use_container_width=True)

                if submit:
                    if not new_name or not new_email or not new_password:
                        st.error("Please fill all fields")
                    else:
                        users_db = load_users()
                        if new_email in users_db:
                            st.error("User already exists")
                        else:
                            if save_user(new_email, new_password, new_name, new_role):
                                st.success("User added successfully!")
                                st.rerun()

    elif page == "Readings":
        readings_page()

    elif page == "Settings":
        st.markdown(f"""
        <div class="main-header">
            <h1>SETTINGS</h1>
            <div class="header-subtitle">System Configuration</div>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("System Settings")
        st.write("**Monitoring Locations:**")
        for loc in LOCATIONS:
            st.write(f"✓ {loc}")

        st.write("---")
        st.subheader("Your Account")
        st.write(f"**Name:** {st.session_state.user_name}")
        st.write(f"**Email:** {st.session_state.user_email}")
        st.write(f"**Role:** {st.session_state.user_role}")

if __name__ == "__main__":
    # Check if user is logged in
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.error("Please login first!")
        st.stop()
    
    admin_dashboard()