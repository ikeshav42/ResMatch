# ResMatch

ResMatch is an NLP-based web application that compares a resume with a job description and produces a semantic match score.  
Instead of relying purely on keyword overlap, it uses transformer-based embeddings to measure how closely a resume aligns with a role in terms of meaning.

The project is built using **Python, Sentence Transformers, and Streamlit**.

---

## Why I Built This

As a computer science graduate applying for software and machine learning roles, I noticed two recurring problems during job applications:

1. Job descriptions often describe the same skills using different wording.
2. Many resume screening systems rely heavily on keyword matching, which can miss relevant candidates.
3. Too many Job roles out there in the current market.

I built ResMatch to:
- Learn how modern NLP techniques are used in practical applications
- Understand semantic similarity beyond simple keyword matching
- Build an end-to-end ML-backed application rather than isolated models

This project also serves as a hands-on way for me to bridge academic machine learning concepts with real-world software development practices.

---

## What the App Does

ResMatch performs the following steps:

1. Accepts a resume in PDF format
2. Extracts text content from the resume
3. Takes a job description as input
4. Converts both texts into semantic embeddings using a transformer model
5. Computes a similarity score using cosine similarity
6. Displays an interpretable match score through a simple web interface

---

## Tech Stack

- Python  
- Streamlit – frontend and application framework  
- Sentence Transformers – semantic text embeddings  
- PyTorch – model backend  
- pdfplumber – PDF resume text extraction  
- scikit-learn / NumPy – supporting utilities  

---

## Current Limitations

- The similarity score is based on full-text comparison and may be affected by resume formatting or non-relevant sections
- The app currently compares one resume against one job description at a time
- There is no explicit skill-level weighting or section-based scoring yet

---

## Planned Improvements

Future updates will focus on improving relevance and interpretability, including:

- Filtering resume content to focus on skills and project sections
- Identifying missing or weakly represented skills compared to a job description
- Normalizing similarity scores to make them more human-readable
- Supporting comparison against multiple job descriptions
- Improving UI feedback and explanations for match results
---

## Learning Goals

Through this project, I aim to:
- Develop a deeper understanding of transformer-based NLP models
- Practice clean project structuring and reproducible ML environments
- Improve my ability to explain ML systems clearly
- Build practical, application-oriented projects

---

## How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
