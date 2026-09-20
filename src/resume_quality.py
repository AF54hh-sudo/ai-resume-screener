"""Rule-based resume quality analysis."""

from __future__ import annotations

import re

from src.text_cleaner import clean_text


def analyze_resume_quality(resume_text: str) -> dict[str, float | list[str]]:
    """Score basic resume quality signals in an explainable way."""
    text = clean_text(resume_text)
    if not text:
        return {
            "quality_score": 0.0,
            "strengths": [],
            "weaknesses": ["Resume text could not be extracted or is empty."],
        }

    checks: list[tuple[str, bool, str, str]] = [
        (
            "projects",
            bool(re.search(r"\b(project|projects|portfolio)\b", text)),
            "Includes a projects or portfolio section.",
            "Add a projects section with role-relevant work.",
        ),
        (
            "skills section",
            bool(re.search(r"\b(skills|technical skills|technologies)\b", text)),
            "Includes a clear skills or technologies section.",
            "Add a dedicated skills section for quick recruiter scanning.",
        ),
        (
            "education",
            bool(re.search(r"\b(education|degree|bachelor|master|university|college)\b", text)),
            "Mentions education or formal training.",
            "Include education, certifications, or relevant coursework.",
        ),
        (
            "experience",
            bool(re.search(r"\b(experience|internship|work history|employment|developer|analyst|engineer)\b", text)),
            "Mentions experience, internships, or relevant roles.",
            "Add experience or internship bullets with responsibilities and impact.",
        ),
        (
            "tools",
            bool(re.search(r"\b(tools|technologies|python|sql|excel|tableau|power bi|docker|git)\b", text)),
            "References tools or technologies.",
            "Name the tools and technologies used in each project or role.",
        ),
        (
            "measurable impact",
            bool(re.search(r"(\b\d+(\.\d+)?%?\b|\b(increased|reduced|improved|saved|automated|optimized)\b)", text)),
            "Includes numbers or measurable impact.",
            "Quantify outcomes such as accuracy, time saved, cost reduction, or usage.",
        ),
        (
            "links",
            bool(re.search(r"\b(github\.com|linkedin\.com|https?://|www\.)", text)),
            "Includes GitHub, LinkedIn, or portfolio links.",
            "Add GitHub, LinkedIn, or portfolio links near the header.",
        ),
        (
            "clean length",
            250 <= len(text.split()) <= 1200,
            "Resume length looks appropriate for screening.",
            "Keep the resume concise, ideally 1-2 pages with focused bullets.",
        ),
    ]

    strengths = [strength for _, passed, strength, _ in checks if passed]
    weaknesses = [weakness for _, passed, _, weakness in checks if not passed]
    score = round((len(strengths) / len(checks)) * 100, 2)

    return {
        "quality_score": score,
        "strengths": strengths,
        "weaknesses": weaknesses,
    }
