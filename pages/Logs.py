import streamlit as st
import pandas as pd

from app.services.log_service import get_logs

if not st.session_state.get("logged_in"):

    st.warning("Please login first")

    if st.button("Go to Login"):
        st.switch_page("pages/Login.py")

    st.stop()
    
if st.button("← Back"):
    st.switch_page("pages/Dashboard.py")

st.title("Vehicle Logs")

logs = get_logs()

if logs:

    df = pd.DataFrame(
        logs,
        columns=[
            "ID",
            "Car Number",
            "Owner Email",
            "Entry Time",
            "Exit Time"
        ]
    )

    search_plate = st.text_input(
        "Search by Car Number"
    )

    if search_plate:

        df = df[
            df["Car Number"]
            .str.contains(
                search_plate.upper(),
                na=False
            )
        ]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Logs",
            len(df)
        )

    with col2:
        st.metric(
            "Unique Vehicles",
            df["Car Number"].nunique()
        )

    st.dataframe(
        df,
        use_container_width=True
    )

else:
    st.info("No logs found")