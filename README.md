# AI Resume Screener & Job Match Ranker

An AI/NLP-powered Streamlit application that compares resumes against job descriptions, explains fit scores, identifies skill gaps, and ranks multiple resumes for recruiter-style screening workflows.

## Problem Statement

Candidates often struggle to understand how well their resume matches a role, while recruiters need a fast, explainable way to compare resumes against a job description. Basic keyword matching misses semantic overlap and gives weak guidance.

## Solution Overview

This project extracts resume text from PDFs, cleans the text, detects curated technical skills, extracts important keywords, computes semantic similarity with Sentence-Transformers, checks resume quality signals, and combines everything into a weighted match score. It also generates transparent, rule-based suggestions without using paid APIs.

## Features

- Resume PDF upload with robust PyMuPDF text extraction.
- Job description input validation.
- Text normalization and cleaning pipeline.
- Curated skill extraction with aliases such as `scikit learn` to `Scikit-learn`, `gen ai` to `Generative AI`, and `postgres` to `PostgreSQL`.
- Keyword extraction with KeyBERT and a TF-IDF fallback.
- Semantic similarity using `sentence-transformers/all-MiniLM-L6-v2`.
- Weighted scoring across semantic similarity, skill overlap, keyword coverage, and resume quality.
- Explainable resume quality checks for projects, skills, education, experience, links, measurable impact, and length.
- Actionable improvement suggestions.
- Optional multiple resume ranking tab with CSV export.
- Unit tests for core text, skill, and scoring logic.

## Tech Stack

- Python
- Streamlit
- PyMuPDF
- Sentence-Transformers
- KeyBERT
- scikit-learn
- pandas
- NumPy
- pytest

## Architecture Diagram

```text
PDF Resume + Job Description
          |
          v
PDF Parser -> Text Cleaner
          |
          v
Skill Extractor + Keyword Extractor + Semantic Similarity + Quality Checker
          |
          v
Weighted Scoring Engine
          |
          v
Streamlit UI: Scores, Gaps, Strengths, Weaknesses, Suggestions, Ranking CSV
```

## Folder Structure

```text
ai-resume-screener/
|-- app.py
|-- README.md
|-- requirements.txt
|-- .gitignore
|-- src/
|   |-- __init__.py
|   |-- pdf_parser.py
|   |-- text_cleaner.py
|   |-- skill_extractor.py
|   |-- keyword_extractor.py
|   |-- similarity.py
|   |-- scoring.py
|   |-- resume_quality.py
|   |-- suggestions.py
|   |-- ranker.py
|   `-- utils.py
|-- data/
|   |-- sample_resumes/
|   `-- sample_jobs/
|-- outputs/
|   `-- reports/
|-- assets/
|   `-- screenshots/
`-- tests/
    |-- test_text_cleaner.py
    |-- test_skill_extractor.py
    `-- test_scoring.py
```

## How to Run Locally

1. Create and activate a virtual environment.

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Run the Streamlit app.

```bash
streamlit run app.py
```

4. Run tests.

```bash
pytest
```

## Example Use Case

A candidate uploads a data analyst resume and pastes a job description requiring Python, SQL, Power BI, data cleaning, dashboards, and statistics. The app extracts the resume text, compares the resume with the job description, reports matched and missing skills, calculates an overall match score, and suggests targeted improvements such as adding dashboard metrics or naming specific SQL projects.

## Scoring Logic

The final score is weighted as:

```text
Semantic similarity: 50%
Skill match: 30%
Keyword coverage: 15%
Resume quality signals: 5%
```

Fit categories:

```text
80-100: Strong Match
60-79: Moderate Match
40-59: Low Match
0-39: Weak Match
```

## Screenshots

Add screenshots to `assets/screenshots/` after running the app locally.

## Future Improvements

- OCR support for scanned PDF resumes.
- Section-level parsing for experience, projects, education, and skills.
- Configurable skill taxonomy by role family.
- More advanced keyword weighting by job requirement priority.
- Batch report generation as PDF or Excel.
- Optional local LLM-based suggestions while preserving a no-paid-API mode.

## Resume Bullet Points

- Built an AI-powered resume screening application using Python, Streamlit, PyMuPDF, Sentence-Transformers, and cosine similarity to compare resumes against job descriptions.
- Designed a weighted scoring system combining semantic similarity, skill overlap, keyword coverage, and resume quality signals to generate candidate-job fit scores.
- Implemented PDF parsing, skill extraction, keyword matching, missing skill detection, and actionable resume improvement suggestions.
- Extended the system to rank multiple resumes against a single job description and export results for recruiter-style screening workflows.

## Known Limitations

- Scanned or image-only PDFs require OCR, which is not included in V1.
- Semantic models download on first use and require internet access unless cached locally.
- Skill extraction is dictionary-based for explainability, so uncommon tools may need to be added to `SKILL_ALIASES`.
- Keyword extraction falls back to TF-IDF if KeyBERT or its model dependencies are unavailable.
