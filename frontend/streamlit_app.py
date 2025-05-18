import streamlit as st
import requests
import pandas as pd

st.title("AI Job Application Bot")

st.markdown("Upload your resume and enter the role and location you'd like to apply for:")

role = st.text_input("Role")
location = st.text_input("Location")
resume = st.file_uploader("Upload your Resume (PDF or DOCX)", type=["pdf", "docx"])

if st.button("Find and Apply to Jobs"):
    if not role or not location or not resume:
        st.error("Please provide role, location, and resume.")
    else:
        with st.spinner("Applying for jobs..."):
            try:
                # Prepare data for POST request
                files = {'resume': resume}
                data = {'role': role, 'location': location}

                # Send POST request to backend
                response = requests.post("http://localhost:5000/apply", files=files, data=data)

                if response.status_code == 200:
                    result = response.json()
                    st.markdown(result)
                else:
                    st.error(f"Server error: {response.status_code} - {response.text}")
            except Exception as e:
                st.exception(f"An error occurred: {e}")