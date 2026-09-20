"""Shared helper functions for the app and ranking workflow."""

from __future__ import annotations

from src.keyword_extractor import compare_keywords, extract_keywords
from src.resume_quality import analyze_resume_quality
from src.scoring import calculate_final_score
from src.similarity import calculate_semantic_similarity
from src.skill_extractor import compare_skills, extract_skills
from src.suggestions import generate_suggestions
from src.text_cleaner import clean_text


def analyze_resume_against_jd(resume_text: str, jd_text: str) -> dict:
    """Run the full screening pipeline for one resume and one job description."""
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(jd_text)
    if not resume_clean:
        raise ValueError("Resume text is empty.")
    if not jd_clean:
        raise ValueError("Job description is empty.")

    resume_skills = extract_skills(resume_clean)
    jd_skills = extract_skills(jd_clean)
    skill_comparison = compare_skills(resume_skills, jd_skills)

    resume_keywords = extract_keywords(resume_clean, top_n=25)
    jd_keywords = extract_keywords(jd_clean, top_n=25)
    keyword_comparison = compare_keywords(resume_keywords, jd_keywords)

    semantic_score = calculate_semantic_similarity(resume_clean, jd_clean)
    quality_analysis = analyze_resume_quality(resume_text)
    score = calculate_final_score(
        semantic_score=semantic_score,
        skill_score=float(skill_comparison["skill_match_percentage"]),
        keyword_score=float(keyword_comparison["keyword_coverage_percentage"]),
        quality_score=float(quality_analysis["quality_score"]),
    )
    suggestions = generate_suggestions(
        missing_skills=skill_comparison["missing_skills"],
        missing_keywords=keyword_comparison["missing_keywords"],
        fit_category=str(score["fit_category"]),
        quality_analysis=quality_analysis,
    )

    return {
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "resume_keywords": resume_keywords,
        "jd_keywords": jd_keywords,
        "skill_comparison": skill_comparison,
        "keyword_comparison": keyword_comparison,
        "quality_analysis": quality_analysis,
        "score": score,
        "suggestions": suggestions,
    }
