import streamlit as st
import os
import uuid
import re

from app.services.vehicle_service import register_vehicle

if st.button("← Back"):
    st.switch_page("pages/Dashboard.py")


st.title("Vehicle Registration")

with st.form("vehicle_form"):

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

    car_no = st.text_input("Car Number")

    chassis_no = st.text_input(
        "Chassis Number"
    )

    uploaded_file = st.file_uploader(
        "Vehicle Photo",
        type=["jpg", "jpeg", "png"]
    )

    submitted = st.form_submit_button(
        "Register Vehicle"
    )

if submitted:

    if not all([
        fullname,
        address,
        email,
        phone,
        car_no,
        chassis_no,
        uploaded_file
    ]):
        st.error("All fields required")

    elif not re.match(
        r"[^@]+@[^@]+\.[^@]+",
        email
    ):
        st.error("Invalid email")

    elif not phone.isdigit() or len(phone) != 10:
        st.error("Invalid phone number")

    else:

        os.makedirs(
            "uploads",
            exist_ok=True
        )

        ext = os.path.splitext(
            uploaded_file.name
        )[1]

        filename = (
            f"{car_no.upper()}_"
            f"{uuid.uuid4().hex[:6]}"
            f"{ext}"
        )

        save_path = os.path.abspath(
            os.path.join(
                "uploads",
                filename
            )
        )

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        register_vehicle(
            fullname,
            address,
            email,
            phone,
            1 if gender == "Male" else 2,
            age,
            save_path,
            car_no.upper(),
            chassis_no
        )

        st.success(
            "Vehicle Registered Successfully"
        )
        st.switch_page("pages/Dashboard.py")