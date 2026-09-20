from src.skill_extractor import compare_skills, extract_skills


def test_extract_skills_handles_aliases():
    text = "Built Gen AI apps with scikit learn, postgres, and PowerBI."
    skills = extract_skills(text)
    assert "Generative AI" in skills
    assert "Scikit-learn" in skills
    assert "PostgreSQL" in skills
    assert "Power BI" in skills


def test_compare_skills_reports_missing_and_percentage():
    result = compare_skills(["Python", "SQL"], ["Python", "SQL", "Docker"])
    assert result["matched_skills"] == ["Python", "SQL"]
    assert result["missing_skills"] == ["Docker"]
    assert result["skill_match_percentage"] == 66.67
