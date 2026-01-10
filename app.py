import sys
import os
import tempfile
import streamlit as st

sys.path.append(os.path.abspath("src"))

from resume_parser import extract_text_from_pdf
from matcher import match_jd_to_resume

st.set_page_config(page_title="ResMatch", layout="centered")

st.title("📄 ResMatch")
st.write("Check how well your resume covers a job description using semantic matching.")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description", height=220)


if st.button("Match Resume"):
    if uploaded_file is None or not job_description.strip():
        st.warning("Please upload a resume and paste a job description.")
        st.stop()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        resume_path = tmp.name

    resume_text = extract_text_from_pdf(resume_path)

    score, matches = match_jd_to_resume(resume_text, job_description)

    st.success(f"🔍 Match Score: **{score * 100:.2f}%**")

    if score >= 0.7:
        st.write("✅ Strong coverage of most job requirements.")
    elif score >= 0.45:
        st.write("⚠️ Partial coverage — some requirements are well supported.")
    else:
        st.write("⚠️ Limited coverage — several job requirements lack evidence.")

    st.subheader("📌 Job Requirement Coverage")

    for m in matches:
        st.markdown(f"""
**JD Requirement:** {m['jd']}  
→ **Best Resume Evidence:** {m['resume']}  
Similarity: `{m['score']:.2f}`
---
""")
