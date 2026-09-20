"""Semantic similarity using Sentence-Transformers."""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
import math
import re

import numpy as np

from src.text_cleaner import clean_text


DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=2)
def load_embedding_model(model_name: str = DEFAULT_MODEL_NAME):
    """Load and cache the embedding model so repeated analyses are fast."""
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(model_name)


def _cosine_score(vector_a, vector_b) -> float:
    try:
        from sklearn.metrics.pairwise import cosine_similarity

        return float(cosine_similarity([vector_a], [vector_b])[0][0])
    except Exception:
        dot_product = float(np.dot(vector_a, vector_b))
        denominator = float(np.linalg.norm(vector_a) * np.linalg.norm(vector_b))
        return dot_product / denominator if denominator else 0.0


def _calculate_lexical_similarity(resume_text: str, jd_text: str) -> float:
    resume_tokens = re.findall(r"\b[a-zA-Z][a-zA-Z0-9+#.-]{1,}\b", resume_text)
    jd_tokens = re.findall(r"\b[a-zA-Z][a-zA-Z0-9+#.-]{1,}\b", jd_text)
    resume_counts = Counter(resume_tokens)
    jd_counts = Counter(jd_tokens)
    vocabulary = sorted(set(resume_counts) | set(jd_counts))
    if not vocabulary:
        return 0.0

    resume_vector = np.array([resume_counts[token] for token in vocabulary], dtype=float)
    jd_vector = np.array([jd_counts[token] for token in vocabulary], dtype=float)
    score = _cosine_score(resume_vector, jd_vector)
    return round(float(max(0.0, min(1.0, score))) * 100, 2)


def calculate_semantic_similarity(
    resume_text: str,
    jd_text: str,
    model_name: str = DEFAULT_MODEL_NAME,
) -> float:
    """Calculate cosine similarity between resume and JD embeddings as a percentage."""
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(jd_text)
    if len(resume_clean) < 20 or len(jd_clean) < 20:
        return 0.0

    try:
        model = load_embedding_model(model_name)
        embeddings = model.encode([resume_clean, jd_clean], convert_to_numpy=True)
        score = _cosine_score(embeddings[0], embeddings[1])
        percentage = float(np.clip(score, 0, 1) * 100)
        return round(percentage, 2)
    except Exception:
        return _calculate_lexical_similarity(resume_clean, jd_clean)
