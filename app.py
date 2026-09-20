"""Streamlit app for AI Resume Screener & Job Match Ranker."""

from __future__ import annotations

from html import escape

import streamlit as st

from src.pdf_parser import PDFExtractionError, extract_text_from_pdf
from src.ranker import rank_resumes
from src.utils import analyze_resume_against_jd


st.set_page_config(
    page_title="AI Resume Screener & Job Match Ranker",
    page_icon="resume",
    layout="wide",
)


def apply_custom_styles() -> None:
    """Apply a polished dashboard theme to the Streamlit app."""
    st.markdown(
        """
        <style>
        :root {
            --ink: #102033;
            --muted: #5d6f82;
            --panel: rgba(255, 255, 255, 0.86);
            --line: rgba(55, 92, 128, 0.16);
            --teal: #0f9f9a;
            --teal-dark: #087b79;
            --coral: #ff6b5f;
            --amber: #f4b740;
            --green: #25a76f;
            --red: #d9485f;
        }

        .stApp {
            background:
                radial-gradient(circle at 12% 12%, rgba(15, 159, 154, 0.22), transparent 30%),
                radial-gradient(circle at 88% 8%, rgba(255, 107, 95, 0.18), transparent 28%),
                radial-gradient(circle at 50% 95%, rgba(244, 183, 64, 0.18), transparent 32%),
                linear-gradient(135deg, #f8fcff 0%, #eef7fb 46%, #fff9f1 100%);
            color: var(--ink);
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1180px;
        }

        h1, h2, h3 {
            color: var(--ink);
            letter-spacing: 0;
        }

        div[data-testid="stTabs"] button {
            border-radius: 999px;
            padding: 0.6rem 1rem;
            background: rgba(255, 255, 255, 0.92);
            border: 1px solid rgba(8, 123, 121, 0.2);
            color: var(--ink);
            box-shadow: 0 10px 24px rgba(58, 91, 122, 0.11);
            transition: background 160ms ease, transform 160ms ease, box-shadow 160ms ease;
        }

        div[data-testid="stTabs"] button p {
            color: var(--ink);
            font-weight: 800;
        }

        div[data-testid="stTabs"] button:hover {
            background: #ffffff;
            transform: translateY(-1px);
            box-shadow: 0 14px 30px rgba(58, 91, 122, 0.16);
        }

        div[data-testid="stTabs"] button[aria-selected="true"] {
            background: linear-gradient(135deg, var(--teal), var(--teal-dark));
            color: #ffffff;
        }

        div[data-testid="stTabs"] button[aria-selected="true"] p {
            color: #ffffff;
        }

        div[data-testid="stTabs"] div[data-baseweb="tab-list"] {
            gap: 0.55rem;
            padding: 0.35rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.42);
            border: 1px solid rgba(55, 92, 128, 0.12);
            backdrop-filter: blur(10px);
        }

        div[data-testid="stFileUploader"],
        div[data-testid="stTextArea"] textarea {
            border-radius: 16px;
        }

        div[data-testid="stFileUploader"] {
            padding: 0.8rem;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.72);
            border: 1px solid var(--line);
        }

        div[data-testid="stTextArea"] textarea {
            background: rgba(255, 255, 255, 0.88);
            border: 1px solid rgba(8, 123, 121, 0.18);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.7);
        }

        div.stButton > button,
        div.stDownloadButton > button {
            border: 0;
            border-radius: 999px;
            padding: 0.75rem 1.35rem;
            color: #ffffff;
            background: linear-gradient(135deg, var(--teal), #18b6a7);
            box-shadow: 0 14px 28px rgba(15, 159, 154, 0.25);
            transition: transform 160ms ease, box-shadow 160ms ease;
        }

        div.stButton > button:hover,
        div.stDownloadButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 18px 34px rgba(15, 159, 154, 0.32);
        }

        .hero {
            position: relative;
            overflow: hidden;
            border-radius: 28px;
            padding: 2rem;
            margin-bottom: 1.2rem;
            background:
                linear-gradient(115deg, rgba(255,255,255,0.06) 0 14%, transparent 14% 26%, rgba(255,255,255,0.05) 26% 40%, transparent 40%),
                linear-gradient(135deg, rgba(16, 32, 51, 0.92), rgba(8, 123, 121, 0.86)),
                radial-gradient(circle at 88% 18%, rgba(244, 183, 64, 0.35), transparent 28%);
            box-shadow: 0 28px 70px rgba(28, 63, 88, 0.24);
            color: #ffffff;
        }

        .hero:after {
            content: "";
            position: absolute;
            width: 260px;
            height: 260px;
            right: -70px;
            bottom: -100px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.12);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }

        .eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.42rem 0.78rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.14);
            border: 1px solid rgba(255, 255, 255, 0.22);
            color: #e9fffb;
            font-size: 0.82rem;
            font-weight: 700;
            text-transform: uppercase;
        }

        .hero h1 {
            margin: 0.8rem 0 0.55rem 0;
            color: #ffffff;
            font-size: 2.55rem;
            line-height: 1.05;
        }

        .hero p {
            max-width: 760px;
            color: rgba(255, 255, 255, 0.86);
            font-size: 1.02rem;
            margin-bottom: 1.1rem;
        }

        .hero-stats {
            display: flex;
            flex-wrap: wrap;
            gap: 0.7rem;
        }

        .hero-stat {
            padding: 0.75rem 0.9rem;
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.12);
            border: 1px solid rgba(255, 255, 255, 0.16);
            min-width: 140px;
            transition: transform 160ms ease, background 160ms ease;
        }

        .hero-stat:hover {
            transform: translateY(-2px);
            background: rgba(255, 255, 255, 0.18);
        }

        .hero-stat strong {
            display: block;
            color: #ffffff;
            font-size: 1rem;
        }

        .hero-stat span {
            color: rgba(255, 255, 255, 0.74);
            font-size: 0.82rem;
        }

        .glass-panel {
            padding: 1.1rem;
            border-radius: 22px;
            background: var(--panel);
            border: 1px solid var(--line);
            box-shadow: 0 16px 45px rgba(58, 91, 122, 0.14);
            backdrop-filter: blur(12px);
            margin: 0.8rem 0;
            position: relative;
            overflow: hidden;
        }

        .glass-panel:before {
            content: "";
            position: absolute;
            inset: 0 auto 0 0;
            width: 5px;
            background: linear-gradient(180deg, var(--teal), var(--amber));
        }

        .section-title {
            font-size: 1.2rem;
            font-weight: 800;
            margin: 0 0 0.55rem 0;
            color: var(--ink);
        }

        .muted {
            color: var(--muted);
            font-size: 0.94rem;
        }

        .score-card {
            padding: 1.25rem;
            border-radius: 24px;
            background:
                radial-gradient(circle at 92% 12%, rgba(244, 183, 64, 0.22), transparent 24%),
                linear-gradient(135deg, rgba(255,255,255,0.96), rgba(241,250,249,0.9));
            border: 1px solid var(--line);
            box-shadow: 0 18px 50px rgba(53, 82, 111, 0.16);
        }

        .score-value {
            font-size: 3rem;
            line-height: 1;
            font-weight: 900;
            color: var(--teal-dark);
            margin: 0.25rem 0;
        }

        .fit-badge {
            display: inline-flex;
            padding: 0.48rem 0.85rem;
            border-radius: 999px;
            color: #ffffff;
            background: linear-gradient(135deg, var(--teal), var(--green));
            font-weight: 800;
        }

        .component-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.8rem;
            margin: 0.8rem 0 1rem;
        }

        .component-card {
            padding: 1rem;
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.78);
            border: 1px solid var(--line);
            transition: transform 160ms ease, box-shadow 160ms ease;
        }

        .component-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 14px 30px rgba(53, 82, 111, 0.13);
        }

        .component-card span {
            display: block;
            color: var(--muted);
            font-size: 0.82rem;
            font-weight: 700;
        }

        .component-card strong {
            display: block;
            margin-top: 0.25rem;
            color: var(--ink);
            font-size: 1.55rem;
        }

        .chip-wrap {
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
            margin-top: 0.45rem;
        }

        .chip {
            display: inline-flex;
            align-items: center;
            border-radius: 999px;
            padding: 0.42rem 0.68rem;
            background: #e7fbf8;
            color: #076765;
            border: 1px solid rgba(15, 159, 154, 0.22);
            font-weight: 700;
            font-size: 0.86rem;
        }

        .chip.missing {
            background: #fff1ed;
            color: #a33d33;
            border-color: rgba(255, 107, 95, 0.24);
        }

        .chip.keyword {
            background: #fff8e8;
            color: #7b560d;
            border-color: rgba(244, 183, 64, 0.35);
        }

        .signal {
            padding: 0.72rem 0.82rem;
            border-radius: 15px;
            margin: 0.45rem 0;
            border: 1px solid var(--line);
            background: rgba(255, 255, 255, 0.72);
        }

        .signal.good {
            border-left: 5px solid var(--green);
        }

        .signal.warn {
            border-left: 5px solid var(--coral);
        }

        .suggestion-card {
            padding: 0.85rem 1rem;
            border-radius: 16px;
            margin: 0.55rem 0;
            background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(238,247,251,0.86));
            border: 1px solid var(--line);
        }

        @media (max-width: 900px) {
            .component-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .hero h1 {
                font-size: 2rem;
            }
        }

        @media (max-width: 640px) {
            .component-grid {
                grid-template-columns: 1fr;
            }

            .hero {
                padding: 1.25rem;
                border-radius: 22px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    st.markdown(
        """
        <section class="hero">
            <div class="eyebrow">AI screening dashboard</div>
            <h1>AI Resume Screener & Job Match Ranker</h1>
            <p>
                Compare resumes against job descriptions with explainable NLP signals,
                skill gaps, quality checks, and recruiter-style ranking.
            </p>
            <div class="hero-stats">
                <div class="hero-stat"><strong>Semantic Fit</strong><span>meaning-aware matching</span></div>
                <div class="hero-stat"><strong>Skill Gaps</strong><span>matched and missing skills</span></div>
                <div class="hero-stat"><strong>Resume Signals</strong><span>quality and impact checks</span></div>
                <div class="hero-stat"><strong>Batch Ranking</strong><span>CSV-ready shortlist</span></div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_panel(title: str, body: str | None = None) -> None:
    body_html = f'<p class="muted">{escape(body)}</p>' if body else ""
    st.markdown(
        f'<div class="glass-panel"><div class="section-title">{escape(title)}</div>{body_html}</div>',
        unsafe_allow_html=True,
    )


def render_list(items: list[str], empty_message: str) -> None:
    """Render a compact list of items as Streamlit pills."""
    if not items:
        st.markdown(f'<p class="muted">{escape(empty_message)}</p>', unsafe_allow_html=True)
        return
    chips = "".join(f'<span class="chip">{escape(str(item))}</span>' for item in items)
    st.markdown(f'<div class="chip-wrap">{chips}</div>', unsafe_allow_html=True)


def render_missing_list(items: list[str], empty_message: str) -> None:
    if not items:
        st.markdown(f'<p class="muted">{escape(empty_message)}</p>', unsafe_allow_html=True)
        return
    chips = "".join(f'<span class="chip missing">{escape(str(item))}</span>' for item in items)
    st.markdown(f'<div class="chip-wrap">{chips}</div>', unsafe_allow_html=True)


def render_keyword_list(items: list[str], empty_message: str, missing: bool = False) -> None:
    if not items:
        st.markdown(f'<p class="muted">{escape(empty_message)}</p>', unsafe_allow_html=True)
        return
    chip_class = "chip missing" if missing else "chip keyword"
    chips = "".join(f'<span class="{chip_class}">{escape(str(item))}</span>' for item in items)
    st.markdown(f'<div class="chip-wrap">{chips}</div>', unsafe_allow_html=True)


def render_score_breakdown(score: dict) -> None:
    cards = [
        ("Semantic Similarity", score["semantic_score"]),
        ("Skill Match", score["skill_score"]),
        ("Keyword Coverage", score["keyword_score"]),
        ("Resume Quality", score["quality_score"]),
    ]
    cards_html = "".join(
        f'<div class="component-card"><span>{escape(label)}</span><strong>{value:.1f}%</strong></div>'
        for label, value in cards
    )
    st.markdown(f'<div class="component-grid">{cards_html}</div>', unsafe_allow_html=True)


def render_signal_list(items: list[str], empty_message: str, state: str) -> None:
    if not items:
        st.markdown(f'<p class="muted">{escape(empty_message)}</p>', unsafe_allow_html=True)
        return
    html = "".join(f'<div class="signal {state}">{escape(str(item))}</div>' for item in items)
    st.markdown(html, unsafe_allow_html=True)


def render_suggestions(suggestions: list[str]) -> None:
    html = "".join(
        f'<div class="suggestion-card"><strong>Action:</strong> {escape(str(suggestion))}</div>'
        for suggestion in suggestions
    )
    st.markdown(html, unsafe_allow_html=True)


def analyze_single_resume() -> None:
    st.markdown(
        '<div class="glass-panel"><div class="section-title">Start A Resume Match</div>'
        '<p class="muted">Upload one resume, paste the target job description, and get an explainable fit report.</p></div>',
        unsafe_allow_html=True,
    )

    input_col, jd_col = st.columns([0.9, 1.4])
    with input_col:
        uploaded_file = st.file_uploader("Upload resume PDF", type=["pdf"])
    with jd_col:
        jd_text = st.text_area(
            "Paste job description",
            height=240,
            placeholder="Paste the full job description here...",
        )

    if not st.button("Analyze Resume", type="primary"):
        return

    if uploaded_file is None:
        st.error("Please upload a resume PDF.")
        return
    if not jd_text.strip():
        st.error("Please paste a job description.")
        return

    with st.spinner("Extracting resume text and running NLP analysis..."):
        try:
            resume_text = extract_text_from_pdf(uploaded_file)
            analysis = analyze_resume_against_jd(resume_text, jd_text)
        except PDFExtractionError as exc:
            st.error(str(exc))
            return
        except Exception as exc:
            st.error(f"Analysis failed: {exc}")
            return

    score = analysis["score"]
    skills = analysis["skill_comparison"]
    keywords = analysis["keyword_comparison"]
    quality = analysis["quality_analysis"]

    st.markdown(
        f"""
        <div class="score-card">
            <div class="muted">Overall Match Score</div>
            <div class="score-value">{score['overall_score']:.1f}%</div>
            <span class="fit-badge">{escape(str(score["fit_category"]))}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(int(score["overall_score"]))

    st.markdown('<div class="section-title">Score Breakdown</div>', unsafe_allow_html=True)
    render_score_breakdown(score)

    skill_col, gap_col = st.columns(2)
    with skill_col:
        render_panel("Matched Skills")
        render_list(skills["matched_skills"], "No matched skills found.")
    with gap_col:
        render_panel("Missing Skills")
        render_missing_list(skills["missing_skills"], "No missing JD skills found.")

    keyword_col, missing_keyword_col = st.columns(2)
    with keyword_col:
        render_panel("Matched Keywords")
        render_keyword_list(keywords["matched_keywords"], "No matched keywords found.")
    with missing_keyword_col:
        render_panel("Missing Keywords")
        render_keyword_list(keywords["missing_keywords"], "No missing keywords found.", missing=True)

    strength_col, weakness_col = st.columns(2)
    with strength_col:
        render_panel("Resume Strengths")
        render_signal_list(quality["strengths"], "No strengths detected yet.", "good")
    with weakness_col:
        render_panel("Resume Weaknesses")
        render_signal_list(quality["weaknesses"], "No major weaknesses detected.", "warn")

    render_panel("Improvement Suggestions", "Practical edits you can make before applying.")
    render_suggestions(analysis["suggestions"])


def analyze_multiple_resumes() -> None:
    st.markdown(
        '<div class="glass-panel"><div class="section-title">Rank Multiple Resumes</div>'
        '<p class="muted">Upload several resumes and produce a recruiter-style ranked shortlist for one JD.</p></div>',
        unsafe_allow_html=True,
    )

    upload_col, jd_col = st.columns([0.9, 1.4])
    with upload_col:
        uploaded_files = st.file_uploader(
            "Upload resume PDFs",
            type=["pdf"],
            accept_multiple_files=True,
        )
    with jd_col:
        jd_text = st.text_area(
            "Paste one job description for ranking",
            height=240,
            placeholder="Paste the full job description here...",
            key="ranking_jd",
        )

    if not st.button("Rank Resumes", type="primary"):
        return

    if not uploaded_files:
        st.error("Please upload at least one resume PDF.")
        return
    if not jd_text.strip():
        st.error("Please paste a job description.")
        return

    with st.spinner("Ranking resumes..."):
        ranking_df = rank_resumes(uploaded_files, jd_text)

    if ranking_df.empty:
        st.info("No resumes were ranked.")
        return

    st.markdown('<div class="section-title">Ranking Results</div>', unsafe_allow_html=True)
    st.dataframe(ranking_df, use_container_width=True, hide_index=True)

    csv_bytes = ranking_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download CSV",
        data=csv_bytes,
        file_name="resume_ranking_results.csv",
        mime="text/csv",
    )


def main() -> None:
    apply_custom_styles()
    render_hero()

    tab_single, tab_ranking = st.tabs(["Single Resume Analysis", "Multiple Resume Ranking"])
    with tab_single:
        analyze_single_resume()
    with tab_ranking:
        analyze_multiple_resumes()


if __name__ == "__main__":
    main()
