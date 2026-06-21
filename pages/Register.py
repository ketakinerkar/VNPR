import streamlit as st

from app.services.user_service import (
    create_user,
    user_exists,
    password_check,
    valid_email
)

if st.button("← Home"):
    st.switch_page("streamlit_app.py")

st.title("User Registration")

with st.form("register_form"):

    fullname = st.text_input("Full Name")
    address = st.text_input("Address")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")

    gender = st.radio(
        "Gender",
        ["Male", "Female"]
    )

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=100
    )

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password"
    )

    submitted = st.form_submit_button(
        "Register"
    )

if submitted:

    if not fullname:
        st.error("Enter valid name")

    elif not address:
        st.error("Enter address")

    elif not valid_email(email):
        st.error("Invalid email")

    elif not phone.isdigit() or len(phone) != 10:
        st.error("Invalid phone number")

    elif not password_check(password):
        st.error("Weak password")

    elif password != confirm_password:
        st.error("Passwords do not match")

    elif user_exists(username):
        st.error("Username already exists")

    else:

        create_user(
            fullname,
            address,
            username,
            email,
            phone,
            1 if gender == "Male" else 2,
            age,
            password
        )

        st.success(
            "Account created successfully"
        )

        st.session_state.logged_in = True
        st.session_state.username = username

        st.switch_page("pages/Dashboard.py")