# -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 15:06:13 2025

@author: Sneha Umbrajkar
"""
import streamlit as st
import pandas as pd
from sqlalchemy import text
import hashlib
from dbconn import engine  # your existing engine



def hash_password(password):
   
    return hashlib.sha256(password.encode()).hexdigest()

def create_users_table():
    
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(50) DEFAULT 'user'
            )
        """))

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
    """Authenticate user credentials."""
    hashed_pwd = hash_password(password)
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id, name, email, role FROM users WHERE email=:email AND password=:password"),
            {"email": email, "password": hashed_pwd}
        ).fetchone()
    if result:
        return {"id": result[0], "name": result[1], "email": result[2], "role": result[3]}
    return None

def logout():
    """Logout function."""
    for key in ['logged_in', 'user_name', 'user_email', 'user_role', 'auth_mode']:
        if key in st.session_state:
            del st.session_state[key]
    st.experimental_rerun()

# ------------------ STREAMLIT LOGIN-SIGNUP ------------------

def login_page():
    create_users_table()  # Ensure table exists

    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = 'login'
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        st.success(f"Welcome back, {st.session_state.user_name} ({st.session_state.user_role})!")
        if st.button("Logout", use_container_width=True):
            logout()
    else:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.session_state.auth_mode == 'login':
                st.subheader("Sign In")
                with st.form("login_form"):
                    email = st.text_input("Email")
                    password = st.text_input("Password", type="password")
                    login_clicked = st.form_submit_button("Sign In")
                    if login_clicked:
                        user = authenticate_user(email, password)
                        if user:
                            st.session_state.logged_in = True
                            st.session_state.user_name = user['name']
                            st.session_state.user_email = user['email']
                            st.session_state.user_role = user['role']
                            st.experimental_rerun()
                        else:
                            st.error("Invalid email or password!")

                if st.button("Create New Account", use_container_width=True):
                    st.session_state.auth_mode = 'signup'
                    st.experimental_rerun()

            else:  # signup
                st.subheader("Create Account")
                with st.form("signup_form"):
                    name = st.text_input("Full Name")
                    email = st.text_input("Email")
                    password = st.text_input("Password", type="password")
                    confirm_password = st.text_input("Confirm Password", type="password")
                    signup_clicked = st.form_submit_button("Create Account")
                    if signup_clicked:
                        if password != confirm_password:
                            st.error("Passwords do not match!")
                        elif save_user(name, email, password):
                            st.success("Account created successfully! Please login.")
                            st.session_state.auth_mode = 'login'
                            st.experimental_rerun()
                        else:
                            st.error("Email already registered.")

                if st.button("Sign In", use_container_width=True):
                    st.session_state.auth_mode = 'login'
                    st.experimental_rerun()

# ------------------ RUN ------------------
if __name__ == "__main__":
    login_page()
