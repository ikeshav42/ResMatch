import sys
import os
import tempfile
import streamlit as st

# Make src importable
sys.path.append(os.path.abspath("src"))

from resume_parser import extract_text_from_pdf
from matcher import calculate_similarity

st.set_page_config(page_title="ResMatch", layout="centered")

st.title("📄 ResMatch")
st.write("Match your resume with a job description using NLP")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description", height=200)

if st.button("Match Resume"):
    if uploaded_file is None or not job_description.strip():
        st.warning("Please upload a resume and paste a job description.")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            resume_path = tmp.name

        resume_text = extract_text_from_pdf(resume_path)
        score = calculate_similarity(resume_text, job_description)

        st.success(f"🔍 Match Score: **{score * 100:.2f}%**")

        if score > 0.7:
            st.write("✅ Strong match")
        elif score > 0.5:
            st.write("⚠️ Moderate match")
        else:
            st.write("❌ Weak match")
