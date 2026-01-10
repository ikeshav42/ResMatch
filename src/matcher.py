import re
import numpy as np
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")


def normalize(text: str) -> str:
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_sentences(text: str):
    text = normalize(text)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if len(s.strip()) > 5]


def split_resume_chunks(text: str):

    #Resume → semantic chunks.
    #Bullets, lines treated as key

    text = normalize(text)
    chunks = re.split(r"[•\n]", text)
    return [c.strip() for c in chunks if len(c.strip()) > 8]


def match_jd_to_resume(resume_text: str, job_description: str):
    jd_units = split_sentences(job_description)
    resume_units = split_resume_chunks(resume_text)

    if not jd_units or not resume_units:
        return 0.0, []

    jd_emb = model.encode(jd_units, convert_to_tensor=True)
    resume_emb = model.encode(resume_units, convert_to_tensor=True)

    sim_matrix = util.cos_sim(jd_emb, resume_emb).cpu().numpy()

    matches = []
    scores = []

    for i, jd in enumerate(jd_units):
        best_idx = int(np.argmax(sim_matrix[i]))
        best_score = float(sim_matrix[i][best_idx])

        scores.append(best_score)
        matches.append({
            "jd": jd,
            "resume": resume_units[best_idx],
            "score": best_score
        })

    final_score = float(np.mean(scores))
    matches.sort(key=lambda x: x["score"], reverse=True)

    return final_score, matches
