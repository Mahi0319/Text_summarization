import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from groq import Groq


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SummarAI • Text Summarizer",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()

MODEL_NAME = "openai/gpt-oss-120b"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 0%,
                rgba(91, 33, 182, 0.20),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(37, 99, 235, 0.15),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #07080d 0%,
                #0b0d14 50%,
                #080a10 100%
            );

        color: #f8fafc;
    }

    .main {
        padding-top: 1.5rem;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }


    /* ---------- REMOVE STREAMLIT DEFAULT ---------- */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }


    /* ---------- TYPOGRAPHY ---------- */

    html,
    body,
    [class*="css"] {
        font-family:
            Inter,
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;
    }

    h1,
    h2,
    h3,
    h4 {
        color: #f8fafc !important;
    }

    p {
        color: #94a3b8;
    }


    /* ---------- HERO ---------- */

    .hero-container {
        padding: 34px 38px;
        border-radius: 24px;

        background:
            radial-gradient(
                circle at 90% 10%,
                rgba(124, 58, 237, 0.20),
                transparent 30%
            ),
            radial-gradient(
                circle at 10% 100%,
                rgba(59, 130, 246, 0.12),
                transparent 30%
            ),
            rgba(18, 20, 29, 0.92);

        border: 1px solid rgba(255, 255, 255, 0.09);

        box-shadow:
            0 25px 70px rgba(0, 0, 0, 0.35),
            inset 0 1px 0 rgba(255, 255, 255, 0.04);

        margin-bottom: 30px;
    }


    /* ---------- NATIVE STREAMLIT CONTAINERS ---------- */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(17, 19, 28, 0.72);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        box-shadow:
            0 18px 50px rgba(0, 0, 0, 0.20),
            inset 0 1px 0 rgba(255, 255, 255, 0.025);
    }


    /* ---------- TEXT AREA ---------- */

    textarea {
        background: #10121a !important;
        color: #f8fafc !important;

        border: 1px solid rgba(255, 255, 255, 0.10) !important;
        border-radius: 14px !important;

        font-size: 14px !important;
        line-height: 1.7 !important;

        min-height: 300px !important;

        transition:
            border-color 0.2s ease,
            box-shadow 0.2s ease;
    }

    textarea:focus {
        border-color: rgba(139, 92, 246, 0.85) !important;

        box-shadow:
            0 0 0 1px rgba(139, 92, 246, 0.35),
            0 0 25px rgba(139, 92, 246, 0.10) !important;
    }

    textarea::placeholder {
        color: #64748b !important;
    }


    /* ---------- SELECTBOX ---------- */

    div[data-baseweb="select"] > div {
        background: #11131b !important;
        border: 1px solid rgba(255, 255, 255, 0.10) !important;
        border-radius: 11px !important;
        color: #f8fafc !important;
    }


    /* ---------- BUTTON ---------- */

    .stButton > button {
        width: 100%;

        min-height: 46px;

        border: none !important;
        border-radius: 11px !important;

        background:
            linear-gradient(
                135deg,
                #7c3aed,
                #6366f1
            ) !important;

        color: white !important;

        font-weight: 600 !important;
        font-size: 14px !important;

        box-shadow:
            0 8px 25px rgba(99, 102, 241, 0.25);

        transition:
            transform 0.18s ease,
            box-shadow 0.18s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);

        box-shadow:
            0 12px 32px rgba(99, 102, 241, 0.38);
    }


    /* ---------- DOWNLOAD BUTTON ---------- */

    .stDownloadButton > button {
        border-radius: 11px !important;
        border: 1px solid rgba(255, 255, 255, 0.10) !important;

        background: #151821 !important;
        color: #f8fafc !important;

        font-weight: 600 !important;
    }


    /* ---------- METRICS ---------- */

    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.025);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;

        padding: 14px 16px;
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b !important;
    }

    div[data-testid="stMetricValue"] {
        color: #f8fafc !important;
    }


    /* ---------- LABELS ---------- */

    label {
        color: #cbd5e1 !important;
        font-weight: 500 !important;
    }


    /* ---------- SUCCESS / ERROR / INFO ---------- */

    div[data-testid="stAlert"] {
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }


    /* ---------- DIVIDER ---------- */

    hr {
        border-color: rgba(255, 255, 255, 0.07) !important;
    }


    /* ---------- EXPANDER ---------- */

    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.025);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 12px;
    }


    /* ---------- MOBILE ---------- */

    @media (max-width: 768px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero-container {
            padding: 25px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "source_text" not in st.session_state:
    st.session_state.source_text = ""


# ============================================================
# HERO
# ============================================================

st.markdown('<div class="hero-container">', unsafe_allow_html=True)

st.title("✦ SummarAI")

st.caption(
    "Transform long articles, reports, research papers and notes "
    "into clear, meaningful summaries using fast AI inference."
)

if GROQ_API_KEY:
    st.success("● GROQ API READY")
else:
    st.error("● GROQ API KEY NOT FOUND")

st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# WORKSPACE HEADER
# ============================================================

header_col1, header_col2 = st.columns([4, 1])

with header_col1:
    st.subheader("Summarization Workspace")
    st.caption(
        "Paste your content, configure the AI and generate a professional summary."
    )

with header_col2:
    if GROQ_API_KEY:
        st.success("● API READY")
    else:
        st.warning("● API OFFLINE")


# ============================================================
# MAIN WORKSPACE
# ============================================================

left_col, right_col = st.columns(
    [2.1, 1],
    gap="large"
)


# ============================================================
# SOURCE TEXT
# ============================================================

with left_col:

    with st.container(border=True):

        st.markdown("### 📄 Source Text")

        st.caption(
            "Paste an article, research paper, report, notes or any long-form content."
        )

        source_text = st.text_area(
            "Source content",
            value=st.session_state.source_text,
            height=320,
            placeholder=(
                "Paste your text here...\n\n"
                "Example:\n"
                "Artificial Intelligence is transforming many industries..."
            ),
            label_visibility="collapsed",
        )

        st.session_state.source_text = source_text

        word_count = len(source_text.split()) if source_text.strip() else 0
        character_count = len(source_text)

        metric1, metric2 = st.columns(2)

        with metric1:
            st.metric(
                "WORDS",
                f"{word_count:,}"
            )

        with metric2:
            st.metric(
                "CHARACTERS",
                f"{character_count:,}"
            )


# ============================================================
# AI SETTINGS
# ============================================================

with right_col:

    with st.container(border=True):

        st.markdown("### ⚙️ AI Settings")

        st.caption(
            "Configure how your summary should be generated."
        )

        summary_length = st.selectbox(
            "Summary Length",
            [
                "Concise",
                "Balanced",
                "Detailed"
            ],
            index=1,
        )

        output_format = st.selectbox(
            "Output Format",
            [
                "Paragraph",
                "Bullet Points",
                "Key Points"
            ],
            index=0,
        )

        st.markdown("---")

        st.markdown("**AI Engine**")

        st.caption(
            "Groq • GPT-OSS 120B"
        )

        st.write("")

        generate = st.button(
            "✦ Generate Summary",
            use_container_width=True,
        )


# ============================================================
# GENERATE SUMMARY
# ============================================================

if generate:

    if not GROQ_API_KEY:

        st.error(
            "Groq API key is missing. Add GROQ_API_KEY to your .env file."
        )

    elif not source_text.strip():

        st.warning(
            "Please enter some text before generating a summary."
        )

    elif len(source_text.split()) < 20:

        st.warning(
            "Please enter a longer piece of text. "
            "At least 20 words are recommended."
        )

    else:

        if summary_length == "Concise":
            length_instruction = """
            Create a concise summary.
            Keep only the most important information.
            """

        elif summary_length == "Detailed":
            length_instruction = """
            Create a detailed summary.
            Cover the major ideas, important supporting details,
            facts, names, dates and numbers when present.
            """

        else:
            length_instruction = """
            Create a balanced summary.
            Include the major ideas and important supporting details
            without unnecessary repetition.
            """

        if output_format == "Bullet Points":
            format_instruction = """
            Return the summary as clear bullet points.
            Each bullet should contain one meaningful idea.
            """

        elif output_format == "Key Points":
            format_instruction = """
            Return the summary as concise key points.
            """

        else:
            format_instruction = """
            Return the summary as well-structured paragraphs.
            """

        system_prompt = """
        You are a professional text summarization assistant.

        Your task is to summarize ONLY the text provided by the user.

        Rules:
        1. Do not invent information.
        2. Do not add facts that are not present in the source.
        3. Preserve important names, dates, numbers and facts.
        4. Do not change the meaning of the source.
        5. Do not give your personal opinion.
        6. Remove unnecessary repetition.
        7. Do not begin with phrases such as "Here is the summary".
        8. Produce only the requested summary.
        """

        user_prompt = f"""
        {length_instruction}

        {format_instruction}

        SOURCE TEXT:

        {source_text}
        """

        try:

            client = Groq(
                api_key=GROQ_API_KEY
            )

            with st.spinner("Generating your summary..."):

                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt,
                        },
                        {
                            "role": "user",
                            "content": user_prompt,
                        },
                    ],
                    temperature=0.2,
                    max_completion_tokens=1500,
                )

            summary = response.choices[0].message.content.strip()

            st.session_state.summary = summary

        except Exception as error:

            error_text = str(error)

            if "401" in error_text or "authentication" in error_text.lower():

                st.error(
                    "Authentication failed. Please check your Groq API key."
                )

            elif "429" in error_text:

                st.error(
                    "Groq rate limit reached. Please wait a moment and try again."
                )

            elif "model" in error_text.lower():

                st.error(
                    "The selected AI model could not be used. "
                    "Please verify the Groq model configuration."
                )

            else:

                st.error(
                    "Something went wrong while generating the summary."
                )

                with st.expander("Technical details"):
                    st.code(error_text)


# ============================================================
# SUMMARY RESULT
# ============================================================

if st.session_state.summary:

    st.markdown("")

    with st.container(border=True):

        st.markdown("### ✨ Generated Summary")

        st.caption(
            "AI-generated summary based only on your provided source text."
        )

        st.markdown("---")

        st.markdown(
            st.session_state.summary
        )

        st.markdown("---")

        original_words = len(
            st.session_state.source_text.split()
        )

        summary_words = len(
            st.session_state.summary.split()
        )

        if original_words > 0:

            reduction = (
                (original_words - summary_words)
                / original_words
            ) * 100

            if reduction < 0:
                reduction = 0

        else:
            reduction = 0

        result_col1, result_col2, result_col3 = st.columns(3)

        with result_col1:
            st.metric(
                "ORIGINAL WORDS",
                f"{original_words:,}"
            )

        with result_col2:
            st.metric(
                "SUMMARY WORDS",
                f"{summary_words:,}"
            )

        with result_col3:
            st.metric(
                "REDUCTION",
                f"{reduction:.0f}%"
            )

        st.write("")

        st.download_button(
            label="⬇ Download Summary",
            data=st.session_state.summary,
            file_name="summary.txt",
            mime="text/plain",
            use_container_width=True,
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "SummarAI  •  Powered by Groq  •  Built with Python + Streamlit"
)