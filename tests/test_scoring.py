from src.scoring import calculate_final_score


def test_calculate_final_score_uses_weighted_formula():
    result = calculate_final_score(80, 70, 60, 100)
    assert result["overall_score"] == 75.0
    assert result["fit_category"] == "Moderate Match"


def test_calculate_final_score_clamps_values():
    result = calculate_final_score(150, -10, 50, 100)
    assert result["semantic_score"] == 100.0
    assert result["skill_score"] == 0.0
