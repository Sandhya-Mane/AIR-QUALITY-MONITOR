import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import hashlib

# Configuration
LOCATIONS = [
    "Udyoga Bhawan, Sangli",
    "Rajwada Chowk, Sangli",
    "Kupwad, Sangli"
]

st.set_page_config(
    page_title="Air Quality Monitor",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Authentication functions ---
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def load_users():
    if 'users_db' not in st.session_state:
        st.session_state.users_db = {
            'admin@airquality.com': {
                'password': hash_password('admin123'),
                'name': 'Administrator',
                'role': 'admin',
                'email': 'admin@airquality.com',
                'created_date': 'Jan 15, 2024',
                'status': 'Active'
            }
        }
    return st.session_state.users_db

def save_user(email, password, name, role='user'):
    users_db = load_users()
    users_db[email] = {
        'password': hash_password(password),
        'name': name,
        'role': role,
        'email': email,
        'created_date': datetime.now().strftime('%b %d, %Y'),
        'status': 'Active'
    }
    st.session_state.users_db = users_db

def authenticate_user(email, password):
    users_db = load_users()
    if email in users_db:
        if users_db[email]['password'] == hash_password(password):
            return True, users_db[email]
    return False, None

def logout():
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.session_state.user_name = None
    st.session_state.user_role = None
    st.session_state.current_page = 'login'
    st.rerun()

def delete_user(email):
    users_db = load_users()
    if email in users_db and email != 'admin@airquality.com':
        del users_db[email]
        st.session_state.users_db = users_db
        return True
    return False

def update_user_role(email, new_role):
    users_db = load_users()
    if email in users_db:
        users_db[email]['role'] = new_role
        st.session_state.users_db = users_db
        return True
    return False

# --- Styling ---
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

# --- Login Page ---
def login_page():
    st.markdown(LOGIN_CSS, unsafe_allow_html=True)

    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = 'login'

    col_left, form_container_col, col_right = st.columns([1, 1, 1])

    with form_container_col:
        if st.session_state.auth_mode == 'login':
            st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🌿</div>
                <h1>Air Quality Monitor</h1>
                <p>Sign in to access your environmental dashboard</p>
            </div>
            """, unsafe_allow_html=True)

            with st.form("login_form", clear_on_submit=False):
                email = st.text_input("Email Address", placeholder="Enter your email")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                login_clicked = st.form_submit_button("Sign In", use_container_width=True)

                if login_clicked:
                    if not email or not password:
                        st.error("Please enter both email and password")
                    else:
                        is_auth, user_info = authenticate_user(email, password)
                        if is_auth:
                            st.session_state.logged_in = True
                            st.session_state.user_email = email
                            st.session_state.user_name = user_info['name']
                            st.session_state.user_role = user_info['role']
                            st.session_state.current_page = 'admin' if user_info['role'] == 'admin' else 'dataview'
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error("Invalid email or password")

            st.markdown("<div style='text-align: center; margin-top: 1.8rem; border-top: 1px solid #ddd; padding-top: 1.5rem;'><p>Don't have an account?</p></div>", unsafe_allow_html=True)

            if st.button("Create New Account", key="switch_to_signup", use_container_width=True):
                st.session_state.auth_mode = 'signup'
                st.rerun()

        else:  # Signup
            st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🌿</div>
                <h1>Create Account</h1>
                <p>Join Air Quality Monitor</p>
            </div>
            """, unsafe_allow_html=True)

            with st.form("signup_form", clear_on_submit=False):
                name = st.text_input("Full Name", placeholder="Enter your full name")
                email = st.text_input("Email Address", placeholder="Enter your email")
                password = st.text_input("Password", type="password", placeholder="Create a password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm password")

                signup_clicked = st.form_submit_button("Create Account", use_container_width=True)

                if signup_clicked:
                    if not name or not email or not password or not confirm_password:
                        st.error("Please fill in all fields")
                    elif password != confirm_password:
                        st.error("Passwords do not match")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters")
                    else:
                        users_db = load_users()
                        if email in users_db:
                            st.error("Email already registered")
                        else:
                            save_user(email, password, name, role='user')
                            st.success("Account created! Please log in.")
                            st.session_state.auth_mode = 'login'
                            st.rerun()

            st.markdown("<div style='text-align: center; margin-top: 1.8rem; border-top: 1px solid #ddd; padding-top: 1.5rem;'><p>Already have an account?</p></div>", unsafe_allow_html=True)

            if st.button("Sign In", key="switch_to_login", use_container_width=True):
                st.session_state.auth_mode = 'login'
                st.rerun()

def readings_page():
    """Reading Entry & Recent Readings Page"""
    st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="main-header">
        <h1>AIR QUALITY READINGS</h1>
        <div class="header-subtitle">Record daily measurements</div>
        <div class="user-info">
            Welcome, {st.session_state.user_name}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Daily Data Entry")

    col1, col2, col3 = st.columns(3)
    with col1:
        location = st.selectbox("Select Location", LOCATIONS, key="reading_location")
    with col2:
        reading_date = st.date_input("Date", value=datetime.now(), key="reading_date")
    with col3:
        reading_time = st.time_input("Time", value=datetime.now().time(), key="reading_time")

    st.markdown("#### Pollutant Readings (μg/m³)")

    col1, col2 = st.columns(2)
    with col1:
        so2_val = st.number_input("SO₂ Level", min_value=0.0, max_value=500.0, step=0.1, key="so2_input")
    with col2:
        nox_val = st.number_input("NOₓ Level", min_value=0.0, max_value=500.0, step=0.1, key="nox_input")

    col1, col2 = st.columns(2)
    with col1:
        rspm_val = st.number_input("RSPM Level", min_value=0.0, max_value=500.0, step=0.1, key="rspm_input")
    with col2:
        tspm_val = st.number_input("TSPM Level", min_value=0.0, max_value=500.0, step=0.1, key="tspm_input")

    if st.button("Add Reading", use_container_width=True):
        st.success(f"Reading added for {reading_date} at {reading_time}")

    st.markdown("---")
    st.subheader("Recent Readings")

    recent_readings = pd.DataFrame({
        'DateTime': ['Jan 15, 2:30 PM', 'Jan 14, 2:30 PM', 'Jan 13, 2:30 PM'],
        'Location': [location, location, location],
        'SO₂': [24.5, 23.8, 25.1],
        'NOₓ': [18.3, 19.5, 17.2],
        'RSPM': [45.2, 44.8, 46.5],
        'TSPM': [62.8, 61.5, 63.2],
        'Status': ['Complete', 'Outlier', 'Incomplete']
    })

    st.dataframe(recent_readings, use_container_width=True, hide_index=True)

# --- Data View Page (for normal users) ---
def dataview_page():
    st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)

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
        st.markdown("## Control Panel")
        start_date = st.date_input("Start Date", value=datetime(2024, 1, 1))
        end_date = st.date_input("End Date", value=datetime(2024, 1, 7))
        selected_location = st.selectbox("Monitoring Station", options=LOCATIONS, index=0)
        max_records = st.selectbox("Data Points Limit", options=[500, 1000, 2000, 5000, "All"], index=1)
        apply_filters = st.button("Analyze Data", type="primary", use_container_width=True)
        st.markdown("---")
        if st.session_state.user_role != 'admin':
            if st.button("Logout", key="logout_user_btn", use_container_width=True):
                logout()

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
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.dataframe(df[['SO₂ (μg/m³)', 'NOₓ (μg/m³)', 'RSPM (μg/m³)', 'TSPM (μg/m³)']].describe(), use_container_width=True)

        with tab3:
            st.dataframe(df, use_container_width=True)
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Data", csv_data, f"air_quality_{start_date}_{end_date}.csv", "text/csv")
    else:
        st.info("Configure parameters in the sidebar and click 'Analyze Data' to begin")

# --- Admin Dashboard ---
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
                            save_user(new_email, new_password, new_name, new_role)
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

def generate_air_quality_data(start_date, end_date, location):
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

# --- Main App Logic ---
def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.current_page = 'login'

    if not st.session_state.logged_in:
        login_page()
    else:
        if st.session_state.user_role == 'admin':
            admin_dashboard()
        else:
            dataview_page()

if __name__ == "__main__":
    main()
