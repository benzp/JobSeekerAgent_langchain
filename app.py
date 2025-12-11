# paste the entire streamlit UI code here
from tempfile import NamedTemporaryFile

import os

import streamlit as st
import jobseeker_utils

# =========================
# Streamlit Page Config
# =========================

st.set_page_config(
    page_title="AI Job Assistant",
    layout="wide",
)

st.title("AI Job Search & Resume Assistant")

st.write(
    """
Provide your **current skills/experience** (via resume upload). And provide your ***aspirational role*** (via text input).
"""
)

st.subheader("2️⃣ Current Skills & Experience")
resume = st.file_uploader("Upload your current resume (.pdf, .docx, .txt):")

st.subheader("3️⃣ Aspirational Role")
aspirational_role = st.text_area("Enter the aspirational role(s) you want to apply for:")

submitted = st.button("Search Ideal Jobs")

if submitted:
    # Show what the user provided
    st.write("Submitted!")
    if aspirational_role:
        st.write("Aspirational role:", aspirational_role)
    else:
        st.write("No aspirational role entered.")
    if resume is not None:
        st.write("Uploaded Resume File name:", resume.name)
        resume_contents = jobseeker_utils.extract_text_from_file(resume)
        st.write("Resume Contents:", resume_contents)
        st.subheader("Matched Search Job Results")

        final_output = jobseeker_utils.TopMatchingJobs(aspirational_role, resume_contents)
        st.write(final_output)
    else:
        st.write("No resume uploaded.")

