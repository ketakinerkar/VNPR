import streamlit as st
from app.services.auth_service import authenticate_user

st.set_page_config(layout="centered")

if st.button("← Home"):
    st.switch_page("streamlit_app.py")

st.title("Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):

    if not username or not password:
        st.error("Enter username and password")

    else:

        user = authenticate_user(username, password)

        if user:

            st.success("Login successful")

            st.session_state.logged_in = True
            st.session_state.username = username

            st.switch_page("pages/Dashboard.py")

        else:
            st.error("Invalid username or password")

if st.button("Create Account"):
    st.switch_page("pages/Register.py")