"""Actionable, rule-based resume improvement suggestions."""

from __future__ import annotations


def _top_items(items: list[str], limit: int = 6) -> str:
    return ", ".join(items[:limit])


def generate_suggestions(
    missing_skills: list[str],
    missing_keywords: list[str],
    fit_category: str,
    quality_analysis: dict,
) -> list[str]:
    """Generate practical suggestions from gaps and resume quality signals."""
    suggestions: list[str] = []

    if missing_skills:
        suggestions.append(
            f"Add evidence for high-priority JD skills: {_top_items(missing_skills)}."
        )

    if missing_keywords:
        suggestions.append(
            f"Mirror relevant job-description language where truthful: {_top_items(missing_keywords)}."
        )

    weaknesses = quality_analysis.get("weaknesses", []) if quality_analysis else []
    suggestions.extend(str(weakness) for weakness in weaknesses[:4])

    if fit_category in {"Weak Match", "Low Match"}:
        suggestions.append(
            "Rewrite the summary and top project bullets to directly target this role."
        )
    elif fit_category == "Moderate Match":
        suggestions.append(
            "Strengthen the strongest matching projects with metrics, tools, and business outcomes."
        )
    else:
        suggestions.append(
            "Tailor the first half of the resume with the strongest matched skills to preserve the high fit."
        )

    suggestions.append(
        "Use measurable bullet points such as model accuracy, dashboard adoption, time saved, or data volume handled."
    )

    deduplicated = []
    for suggestion in suggestions:
        if suggestion and suggestion not in deduplicated:
            deduplicated.append(suggestion)
    return deduplicated
