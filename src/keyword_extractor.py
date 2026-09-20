"""Keyword extraction with KeyBERT when available and TF-IDF fallback."""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
import math
import re

from src.text_cleaner import clean_text


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "with",
    "you",
    "your",
}


@lru_cache(maxsize=1)
def _load_keybert_model():
    try:
        from keybert import KeyBERT

        return KeyBERT(model="all-MiniLM-L6-v2")
    except Exception:
        return None


def _extract_keywords_tfidf(text: str, top_n: int) -> list[str]:
    cleaned = clean_text(text)
    if not cleaned:
        return []

    try:
        from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer

        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 3),
            max_features=max(50, top_n * 5),
            token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z0-9+#.-]{1,}\b",
        )
        matrix = vectorizer.fit_transform([cleaned])
        scores = matrix.toarray()[0]
        terms = vectorizer.get_feature_names_out()
        ranked = sorted(zip(terms, scores), key=lambda item: item[1], reverse=True)

        keywords = []
        for term, score in ranked:
            if score <= 0:
                continue
            if term in ENGLISH_STOP_WORDS:
                continue
            keywords.append(term)
            if len(keywords) >= top_n:
                break
        return keywords
    except ValueError:
        return []
    except Exception:
        return _extract_keywords_frequency(cleaned, top_n)


def _extract_keywords_frequency(text: str, top_n: int) -> list[str]:
    tokens = [
        token
        for token in re.findall(r"\b[a-zA-Z][a-zA-Z0-9+#.-]{1,}\b", text)
        if token not in STOP_WORDS and len(token) > 2
    ]
    phrases = tokens[:]
    phrases.extend(" ".join(tokens[index : index + 2]) for index in range(len(tokens) - 1))
    phrases.extend(" ".join(tokens[index : index + 3]) for index in range(len(tokens) - 2))

    counts = Counter(phrases)
    ranked = sorted(counts.items(), key=lambda item: (item[1], math.log(len(item[0]) + 1)), reverse=True)
    return [term for term, _ in ranked[:top_n]]


def extract_keywords(text: str, top_n: int = 20) -> list[str]:
    """Extract important terms from text, preferring KeyBERT with a TF-IDF fallback."""
    cleaned = clean_text(text)
    if not cleaned:
        return []

    model = _load_keybert_model()
    if model is not None:
        try:
            keywords = model.extract_keywords(
                cleaned,
                keyphrase_ngram_range=(1, 3),
                stop_words="english",
                top_n=top_n,
                use_mmr=True,
                diversity=0.65,
            )
            return [keyword for keyword, _ in keywords]
        except Exception:
            pass

    return _extract_keywords_tfidf(cleaned, top_n)


def compare_keywords(resume_keywords: list[str], jd_keywords: list[str]) -> dict[str, list[str] | float]:
    """Compare extracted keyword lists and report JD keyword coverage."""
    resume_set = {clean_text(keyword) for keyword in resume_keywords if clean_text(keyword)}
    jd_set = {clean_text(keyword) for keyword in jd_keywords if clean_text(keyword)}

    matched = sorted(resume_set & jd_set)
    missing = sorted(jd_set - resume_set)
    coverage = (len(matched) / len(jd_set) * 100) if jd_set else 0.0

    return {
        "matched_keywords": matched,
        "missing_keywords": missing,
        "keyword_coverage_percentage": round(coverage, 2),
    }
