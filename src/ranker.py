"""Multiple resume ranking workflow."""

from __future__ import annotations

import pandas as pd

from src.pdf_parser import PDFExtractionError, extract_text_from_pdf
from src.utils import analyze_resume_against_jd


def rank_resumes(uploaded_files, jd_text: str) -> pd.DataFrame:
    """Rank multiple uploaded resumes against one job description."""
    rows = []
    for uploaded_file in uploaded_files or []:
        file_name = getattr(uploaded_file, "name", "uploaded_resume.pdf")
        try:
            resume_text = extract_text_from_pdf(uploaded_file)
            analysis = analyze_resume_against_jd(resume_text, jd_text)
            score = analysis["score"]
            skills = analysis["skill_comparison"]
            rows.append(
                {
                    "Resume File": file_name,
                    "Overall Score": score["overall_score"],
                    "Fit Category": score["fit_category"],
                    "Matched Skills": ", ".join(skills["matched_skills"]),
                    "Missing Skills": ", ".join(skills["missing_skills"]),
                    "Status": "Analyzed",
                }
            )
        except (PDFExtractionError, ValueError) as exc:
            rows.append(
                {
                    "Resume File": file_name,
                    "Overall Score": 0.0,
                    "Fit Category": "Weak Match",
                    "Matched Skills": "",
                    "Missing Skills": "",
                    "Status": str(exc),
                }
            )

    dataframe = pd.DataFrame(rows)
    if dataframe.empty:
        return dataframe

    dataframe = dataframe.sort_values("Overall Score", ascending=False).reset_index(drop=True)
    dataframe.insert(0, "Rank", range(1, len(dataframe) + 1))
    return dataframe
