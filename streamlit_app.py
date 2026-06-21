import streamlit as st

st.set_page_config(
    page_title="VNPR",
    layout="wide"
)

st.title("Vehicle Number Plate Recognition System")

st.subheader("Drive for safety..save life")

col1, col2 = st.columns([2, 1])

with col1:
    st.image("images/bg.jpg", use_container_width=True)

with col2:

    if st.button("Login", use_container_width=True):
        st.switch_page("pages/Login.py")

    if st.button("Register", use_container_width=True):
        st.switch_page("pages/Register.py")