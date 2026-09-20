from src.text_cleaner import clean_text, normalize_text


def test_normalize_text_collapses_whitespace():
    assert normalize_text(" Python   Developer\n\n\nSQL ") == "Python Developer\n\nSQL"


def test_clean_text_preserves_email_and_url_tokens():
    text = "Email: PERSON@example.com | Portfolio: https://example.com"
    cleaned = clean_text(text)
    assert "person@example.com" in cleaned
    assert "https://example.com" in cleaned


def test_clean_text_handles_empty_input():
    assert clean_text("") == ""
