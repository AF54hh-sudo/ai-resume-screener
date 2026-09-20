"""Explainable skill extraction based on a curated alias dictionary."""

from __future__ import annotations

import re

from src.text_cleaner import clean_text


SKILL_ALIASES: dict[str, list[str]] = {
    "Python": ["python", "py"],
    "SQL": ["sql", "structured query language"],
    "Java": ["java"],
    "C++": ["c++", "cpp"],
    "JavaScript": ["javascript", "java script", "js"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy", "num py"],
    "Excel": ["excel", "microsoft excel", "ms excel"],
    "Statistics": ["statistics", "statistical analysis", "stats"],
    "Data Cleaning": ["data cleaning", "data cleansing"],
    "EDA": ["eda", "exploratory data analysis"],
    "Data Visualization": ["data visualization", "data visualisation", "visualization", "visualisation"],
    "Machine Learning": ["machine learning", "ml"],
    "Scikit-learn": ["scikit-learn", "scikit learn", "sklearn", "sci kit learn"],
    "Regression": ["regression"],
    "Classification": ["classification"],
    "Clustering": ["clustering"],
    "Feature Engineering": ["feature engineering", "feature extraction", "feature selection"],
    "Model Evaluation": ["model evaluation", "model validation", "metrics"],
    "XGBoost": ["xgboost", "xg boost"],
    "Random Forest": ["random forest", "random forests"],
    "Logistic Regression": ["logistic regression"],
    "Deep Learning": ["deep learning", "dl"],
    "TensorFlow": ["tensorflow", "tensor flow"],
    "PyTorch": ["pytorch", "py torch"],
    "NLP": ["nlp", "natural language processing"],
    "Computer Vision": ["computer vision", "cv"],
    "Transformers": ["transformers", "transformer models"],
    "LLM": ["llm", "llms", "large language model", "large language models"],
    "RAG": ["rag", "retrieval augmented generation", "retrieval-augmented generation"],
    "Generative AI": ["generative ai", "gen ai", "genai"],
    "Agentic AI": ["agentic ai", "ai agents", "agentic workflows"],
    "Power BI": ["power bi", "powerbi"],
    "Tableau": ["tableau"],
    "Looker": ["looker"],
    "FastAPI": ["fastapi", "fast api"],
    "Flask": ["flask"],
    "Streamlit": ["streamlit"],
    "Docker": ["docker", "containerization", "containers"],
    "Git": ["git", "version control"],
    "GitHub": ["github", "git hub"],
    "REST API": ["rest api", "restful api", "rest apis", "restful services"],
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure", "microsoft azure"],
    "GCP": ["gcp", "google cloud", "google cloud platform"],
    "MySQL": ["mysql", "my sql"],
    "PostgreSQL": ["postgresql", "postgres", "postgre sql"],
    "MongoDB": ["mongodb", "mongo db"],
    "SQLite": ["sqlite", "sqlite3"],
}


def _alias_pattern(alias: str) -> re.Pattern[str]:
    escaped = re.escape(alias.lower()).replace(r"\ ", r"[\s/+_-]+")
    return re.compile(rf"(?<![a-z0-9]){escaped}(?![a-z0-9])", flags=re.IGNORECASE)


def extract_skills(text: str) -> list[str]:
    """Extract canonical skill names from text using case-insensitive aliases."""
    cleaned = clean_text(text)
    if not cleaned:
        return []

    found = []
    for canonical_skill, aliases in SKILL_ALIASES.items():
        if any(_alias_pattern(alias).search(cleaned) for alias in aliases):
            found.append(canonical_skill)
    return found


def compare_skills(resume_skills: list[str], jd_skills: list[str]) -> dict[str, list[str] | float]:
    """Compare resume and job description skills using canonical skill names."""
    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    matched = sorted(resume_set & jd_set)
    missing = sorted(jd_set - resume_set)
    resume_only = sorted(resume_set - jd_set)
    match_percentage = (len(matched) / len(jd_set) * 100) if jd_set else 0.0

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "resume_only_skills": resume_only,
        "skill_match_percentage": round(match_percentage, 2),
    }
