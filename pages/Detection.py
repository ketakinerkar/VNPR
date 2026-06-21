import streamlit as st
import requests
import os

col1, col2 = st.columns([1, 5])

with col1:
    if st.button("← Back"):
        st.switch_page("pages/Dashboard.py")

st.title("Number Plate Recognition")

uploaded_file = st.camera_input(
    "Capture Vehicle Image"
)

if uploaded_file:

    st.image(
        uploaded_file,
        caption="Captured Image",
        use_container_width=True
    )

    with st.spinner("Detecting Number Plate..."):

        response = requests.post(
            "http://127.0.0.1:8000/detect",
            files={
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    uploaded_file.type
                )
            }
        )

        result = response.json()

    if result["status"] == "authorized":

        st.success("Authorized Vehicle Detected")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Detected Plate",
                result["detected"]
            )

        with col2:
            st.metric(
                "Matched Plate",
                result["corrected"]
            )

        with col3:
            st.metric(
                "Confidence",
                f"{result['confidence']}%"
            )

        data = result["data"]

        st.divider()

        img_col, details_col = st.columns([1, 2])

        with img_col:

            if os.path.exists(data[6]):
                st.image(
                    data[6],
                    caption="Registered Vehicle",
                    use_container_width=True
                )

        with details_col:

            st.subheader("Owner Information")

            st.write(f"**Name:** {data[0]}")
            st.write(f"**Address:** {data[1]}")
            st.write(f"**Email:** {data[2]}")
            st.write(f"**Phone:** {data[3]}")
            st.write(f"**Gender:** {'Male' if data[4] == 1 else 'Female'}")
            st.write(f"**Age:** {data[5]}")
            st.write(f"**Vehicle Number:** {data[7]}")
            st.write(f"**Chassis Number:** {data[8]}")

    elif result["status"] == "unauthorized":
        st.error("Unauthorized Vehicle")

    elif result["status"] == "no_plate":
        st.warning("No Number Plate Detected")

    elif result["status"] == "ocr_failed":
        st.warning("OCR Failed")

    elif result["status"] == "no_match":
        st.warning("No Matching Vehicle Found")

    else:
        st.error(result["status"])

    if st.button("Capture Another Vehicle"):
        st.rerun()