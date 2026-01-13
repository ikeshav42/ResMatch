import sys
import os
import tempfile
import streamlit as st


sys.path.append(os.path.abspath("src"))

from resume_parser import extract_text_from_pdf
from matcher import match_jd_to_resume


st.set_page_config(page_title="ResMatch", layout="centered")

def load_css(file_path: str):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("styles/style.css")

st.title("📄 ResMatch")
st.write(
    "Evaluate how well your resume covers a job description using semantic matching. "
    "The score reflects **JD requirement coverage**, not keyword overlap."
)

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

    st.success(f"JD Coverage Score: **{score * 100:.2f}%**")

    if score >= 0.7:
        st.write("Strong coverage of most job requirements.")
    elif score >= 0.45:
        st.write("Partial coverage — some requirements are well supported.")
    else:
        st.write("Limited coverage — several requirements lack strong evidence.")

    strong = []
    weak = []

    for m in matches:
        if m["score"] >= 0.55:
            strong.append(m)
        else:
            weak.append(m)

    if strong:
        st.subheader("✅ Well Covered Requirements")
        for m in strong:
            st.markdown(
                f"""
**JD Requirement:** {m['jd']}  
→ **Resume Evidence:** {m['resume']}  
*Similarity:* `{m['score']:.2f}`
---
"""
            )
    if weak:
        st.subheader("⚠️ Weak or Missing Requirements")
        for m in weak:
            st.markdown(
                f"""
**JD Requirement:** {m['jd']}  
💡 *No strong, explicit evidence found in the resume. Consider adding a clearer example related to this requirement.*  
*Similarity:* `{m['score']:.2f}`
---
"""
            )
