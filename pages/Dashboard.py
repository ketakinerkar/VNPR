import streamlit as st

st.set_page_config(layout="wide")

if not st.session_state.get("logged_in"):

    st.warning("Please login first")

    if st.button("Go to Login"):
        st.switch_page("pages/Login.py")

    st.stop()

col1, col2, col3 = st.columns([6, 1, 1])

with col3:
    if st.button(
        "Logout",
        use_container_width=True
    ):
        st.session_state.clear()
        st.switch_page("streamlit_app.py")

st.title("Vehicle Number Plate Recognition System")

st.write(
    f"Welcome, {st.session_state.username}"
)

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "Number Plate Registration",
        use_container_width=True
    ):
        st.switch_page(
            "pages/Vehicle_Register.py"
        )

with col2:

    if st.button(
        "Number Plate Recognition",
        use_container_width=True
    ):
        st.switch_page(
            "pages/Detection.py"
        )

st.divider()

if st.button(
    "Vehicle Logs",
    use_container_width=True
):
    st.switch_page(
        "pages/Logs.py"
    )

