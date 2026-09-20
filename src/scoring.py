"""Weighted score calculation for resume-job fit."""

from __future__ import annotations


WEIGHTS = {
    "semantic_score": 0.50,
    "skill_score": 0.30,
    "keyword_score": 0.15,
    "quality_score": 0.05,
}


def _clamp_score(score: float) -> float:
    return max(0.0, min(100.0, float(score or 0.0)))


def _fit_category(overall_score: float) -> str:
    if overall_score >= 80:
        return "Strong Match"
    if overall_score >= 60:
        return "Moderate Match"
    if overall_score >= 40:
        return "Low Match"
    return "Weak Match"


def calculate_final_score(
    semantic_score: float,
    skill_score: float,
    keyword_score: float,
    quality_score: float,
) -> dict[str, float | str]:
    """Combine component scores into an explainable weighted match score."""
    semantic = _clamp_score(semantic_score)
    skill = _clamp_score(skill_score)
    keyword = _clamp_score(keyword_score)
    quality = _clamp_score(quality_score)

    overall = (
        semantic * WEIGHTS["semantic_score"]
        + skill * WEIGHTS["skill_score"]
        + keyword * WEIGHTS["keyword_score"]
        + quality * WEIGHTS["quality_score"]
    )
    overall = round(overall, 2)

    return {
        "overall_score": overall,
        "semantic_score": round(semantic, 2),
        "skill_score": round(skill, 2),
        "keyword_score": round(keyword, 2),
        "quality_score": round(quality, 2),
        "fit_category": _fit_category(overall),
    }
