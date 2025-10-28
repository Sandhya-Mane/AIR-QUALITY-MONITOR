# login_ui.py
import streamlit as st
import hashlib
from sqlalchemy import create_engine
from styles import LOGIN_CSS
from sqlalchemy import text
#from Backend.dbconn import engine, create_users_table
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

import sys, os
print("Python search paths:", sys.path)

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "mini_project_db"
DB_USER = "postgres"
DB_PASS = "root"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
# ---------------- Password Hash ----------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------- Users Table ----------------
#create_users_table()  # Ensure table exists

def save_user(name, email, password, role='user'):
    hashed_pwd = hash_password(password)
    try:
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO users (name, email, password, role) VALUES (:name, :email, :password, :role)"),
                {"name": name, "email": email, "password": hashed_pwd, "role": role}
            )
        return True
    except Exception as e:
        if "duplicate key value violates unique constraint" in str(e):
            return False
        raise e

def authenticate_user(email, password):
    hashed_pwd = hash_password(password)
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id, name, email, role FROM users WHERE email=:email AND password=:password"),
            {"email": email, "password": hashed_pwd}
        ).fetchone()
    if result:
        return {"id": result[0], "name": result[1], "email": result[2], "role": result[3]}
    return None

# ---------------- Logout ----------------
def logout():
    for key in ['logged_in', 'user_name', 'user_email', 'user_role', 'auth_mode']:
        if key in st.session_state:
            del st.session_state[key]
    st.experimental_rerun()

# ---------------- UI ----------------
def login_page():
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = 'login'
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        st.success(f"Welcome back, {st.session_state.user_name} ({st.session_state.user_role})!")
        if st.button("Logout"):
            logout()
    else:
        st.markdown("<h1 style='text-align:center;'>Air Quality Monitor</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center; color:grey;'>Join or Sign In to continue</h3>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if st.session_state.auth_mode == 'login':
                st.subheader("Sign In")
                with st.form("login_form"):
                    email = st.text_input("Email")
                    password = st.text_input("Password", type="password")
                    if st.form_submit_button("Sign In"):
                        user = authenticate_user(email, password)
                        if user:
                            st.session_state.logged_in = True
                            st.session_state.user_name = user['name']
                            st.session_state.user_email = user['email']
                            st.session_state.user_role = user['role']
                            st.experimental_rerun()
                        else:
                            st.error("Invalid email or password!")
                if st.button("Create New Account"):
                    st.session_state.auth_mode = 'signup'
                    st.experimental_rerun()
            else:
                st.subheader("Create Account")
                with st.form("signup_form"):
                    name = st.text_input("Full Name")
                    email = st.text_input("Email")
                    password = st.text_input("Password", type="password")
                    confirm_password = st.text_input("Confirm Password", type="password")
                    if st.form_submit_button("Create Account"):
                        if password != confirm_password:
                            st.error("Passwords do not match!")
                        elif save_user(name, email, password):
                            st.success("Account created successfully! Please login.")
                            st.session_state.auth_mode = 'login'
                            st.experimental_rerun()
                        else:
                            st.error("Email already registered.")
                if st.button("Sign In"):
                    st.session_state.auth_mode = 'login'
                    st.experimental_rerun()

if __name__ == "__main__":
    login_page()
