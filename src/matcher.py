from sentence_transformers import SentenceTransformer, util
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def split_into_sentences(text: str):
    return [s.strip() for s in text.split("\n") if len(s.strip()) > 20]


def weighted_similarity(resume_text: str, job_description: str, top_k_ratio=0.4):
    resume_sentences = split_into_sentences(resume_text)

    if not resume_sentences:
        return 0.0, []

    resume_embeddings = model.encode(resume_sentences, convert_to_tensor=True)
    jd_embedding = model.encode(job_description, convert_to_tensor=True)

    similarities = util.cos_sim(
        resume_embeddings, jd_embedding
    ).cpu().numpy().flatten()

    ranked = sorted(
        zip(resume_sentences, similarities),
        key=lambda x: x[1],
        reverse=True
    )

    k = max(1, int(len(ranked) * top_k_ratio))
    top_sentences = ranked[:k]

    scores = np.array([score for _, score in top_sentences])
    weighted_score = np.sum(scores * scores) / np.sum(scores)

    return float(weighted_score), top_sentences
