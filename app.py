
import os
import streamlit as st
from dotenv import load_dotenv

from rag_pipeline import (
    get_video_id,
    get_transcript,
    create_vector_store,
    answer_question,
)

load_dotenv()

st.set_page_config(
    page_title="Transcript AI | Video Intelligence",
    page_icon="✳️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------- PREMIUM UI STYLES --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #090b12;
    --panel: #111521;
    --panel2: #151b2a;
    --line: #252c3e;
    --text: #f2f4fc;
    --muted: #939cb2;
    --accent: #a78bfa;
    --cyan: #67e8f9;
}

.stApp {
    background:
        radial-gradient(ellipse at 15% 0%, rgba(124,58,237,.13), transparent 35%),
        radial-gradient(ellipse at 90% 20%, rgba(34,211,238,.07), transparent 30%),
        var(--bg);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

header[data-testid="stHeader"] {
    background: rgba(9,11,18,.8);
}

.block-container {
    max-width: 1120px;
    padding-top: 2.2rem;
    padding-bottom: 4rem;
}

h1, h2, h3, p, label {
    font-family: 'DM Sans', sans-serif !important;
}

section[data-testid="stSidebar"] {
    background: var(--panel);
}

.eyebrow {
    display: inline-block;
    padding: 7px 12px;
    border: 1px solid #393052;
    border-radius: 100px;
    background: rgba(167,139,250,.09);
    color: #c4b5fd;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.hero-title {
    font-family: 'Manrope', sans-serif !important;
    font-size: clamp(36px, 5vw, 58px);
    font-weight: 800;
    line-height: 1.12;
    letter-spacing: -2px;
    margin: 20px 0 12px;
    color: #f6f5ff;
}

.gradient-text {
    background: linear-gradient(100deg, #c4b5fd, #818cf8, #67e8f9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-copy {
    color: #a4acc0;
    font-size: 15px;
    line-height: 1.8;
    max-width: 660px;
}

.section-label {
    color: #c7cce0;
    font-size: 12px;
    letter-spacing: 1.7px;
    text-transform: uppercase;
    font-weight: 700;
    margin: 26px 0 12px;
}

div[data-testid="stTextInput"] label,
div[data-testid="stTextArea"] label {
    color: #dce1f1 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background: #111522 !important;
    color: #f4f5fc !important;
    border: 1px solid #2b3247 !important;
    border-radius: 12px !important;
    padding: 13px 15px !important;
    transition: border .2s ease, box-shadow .2s ease;
}

div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: #9b8afb !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,.12) !important;
}

div[data-testid="stTextInput"] input::placeholder,
div[data-testid="stTextArea"] textarea::placeholder {
    color: #6f7890 !important;
}

.stButton > button,
.stLinkButton > a {
    border-radius: 11px !important;
    font-weight: 700 !important;
    min-height: 43px;
    transition: all .2s ease;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(100deg, #8b5cf6, #6366f1) !important;
    color: white !important;
    border: 1px solid #9b8afb !important;
    box-shadow: 0 5px 22px rgba(99,102,241,.18);
}

.stButton > button[kind="primary"]:hover {
    box-shadow: 0 7px 28px rgba(139,92,246,.32);
    border-color: #c4b5fd !important;
    transform: translateY(-1px);
}

.stButton > button:not([kind="primary"]) {
    background: #171c2b !important;
    color: #dce1f1 !important;
    border: 1px solid #30374b !important;
}

.stButton > button:not([kind="primary"]):hover {
    border-color: #8b7ae6 !important;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

div[data-testid="stExpander"] {
    background: rgba(17,21,33,.85);
    border: 1px solid #282f43;
    border-radius: 12px;
    margin-bottom: 10px;
    overflow: hidden;
}

div[data-testid="stExpander"] summary {
    color: #e7e9f7;
    font-size: 13px;
}

.answer-card {
    background: linear-gradient(135deg, #17182c, #111927);
    border: 1px solid #393456;
    border-radius: 17px;
    padding: 24px 25px;
    margin: 12px 0 24px;
    box-shadow: 0 12px 35px rgba(0,0,0,.12);
}

.answer-kicker {
    color: #c4b5fd;
    font-size: 11px;
    letter-spacing: 1.6px;
    text-transform: uppercase;
    font-weight: 700;
    margin-bottom: 14px;
}

.answer-body {
    color: #eef0fc;
    font-size: 16px;
    line-height: 1.85;
    overflow-wrap: anywhere;
}

.stat-card {
    background: rgba(17,21,33,.85);
    border: 1px solid #282f43;
    border-radius: 13px;
    padding: 16px 18px;
    min-height: 84px;
}

.stat-name {
    color: #8f99b0;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-bottom: 7px;
}

.stat-value {
    color: #f0f2ff;
    font-size: 16px;
    font-weight: 700;
}

.footer {
    border-top: 1px solid #242a3a;
    margin-top: 55px;
    padding-top: 20px;
    text-align: center;
    color: #737e96;
    font-size: 12px;
}

div[data-testid="stVideo"] {
    border: 1px solid #2b3247;
    border-radius: 15px;
    overflow: hidden;
}

hr {
    border-color: #252b3b !important;
}

#MainMenu, footer {
    visibility: hidden;
}

@media (max-width: 700px) {
    .block-container {
        padding: 1.2rem 1rem 3rem;
    }
    .hero-title {
        letter-spacing: -1px;
    }
    .answer-card {
        padding: 18px;
    }
}
</style>
""", unsafe_allow_html=True)


# -------------------- HEADER --------------------

left, right = st.columns([3, 1])

with left:
    st.markdown(
        '<span class="eyebrow">✳ AI-POWERED VIDEO INTELLIGENCE</span>',
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        '<div style="text-align:right;color:#9ba5bd;'
        'font-size:12px;padding-top:9px;">GEMINI · FAISS · RAG</div>',
        unsafe_allow_html=True,
    )

st.markdown("""
<div class="hero-title">
    Your videos.<br>
    <span class="gradient-text">Your questions. Answers.</span>
</div>
<div class="hero-copy">
    Turn long YouTube videos into searchable knowledge.
    Ask a question in plain English and explore answers grounded
    in the video's transcript.
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# -------------------- SESSION STATE --------------------

defaults = {
    "indexed_url": None,
    "video_id": None,
    "vector_store": None,
    "chunk_count": 0,
    "last_result": None,
    "last_question": "",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# -------------------- API KEY CHECK --------------------

if not os.getenv("GOOGLE_API_KEY"):
    st.error(
        "Google API key not found. Add GOOGLE_API_KEY to your .env file."
    )
    st.stop()


# -------------------- VIDEO INPUT --------------------

st.markdown(
    '<div class="section-label">01 / SOURCE VIDEO</div>',
    unsafe_allow_html=True,
)

url = st.text_input(
    "YouTube video URL",
    value=st.session_state.indexed_url or "",
    placeholder="Paste a YouTube video link here...",
    help="Use a video with accessible captions. English captions are requested.",
)

load_col, hint_col = st.columns([1, 2])

with load_col:
    load_clicked = st.button(
        "✦  Analyze video",
        type="primary",
        use_container_width=True,
    )

with hint_col:
    st.markdown(
        '<div style="color:#8791a9;font-size:12px;'
        'padding:13px 4px;">Extract transcript · Build semantic index</div>',
        unsafe_allow_html=True,
    )


if load_clicked:
    try:
        video_id = get_video_id(url)

        if (
            st.session_state.video_id == video_id
            and st.session_state.vector_store is not None
        ):
            st.info("This video is already indexed in your current session.")

        else:
            with st.spinner("Extracting captions and building your knowledge index..."):
                snippets = get_transcript(video_id)
                vector_store, chunk_count = create_vector_store(snippets)

            st.session_state.indexed_url = url.strip()
            st.session_state.video_id = video_id
            st.session_state.vector_store = vector_store
            st.session_state.chunk_count = chunk_count
            st.session_state.last_result = None
            st.session_state.last_question = ""

            st.success("Video analyzed successfully. You're ready to ask questions!")

    except Exception as exc:
        st.error(
            "We couldn't analyze this video. Check the URL, caption "
            "availability, and API configuration."
        )
        with st.expander("Technical details"):
            st.code(str(exc))


# -------------------- ACTIVE VIDEO --------------------

if st.session_state.vector_store is not None:
    video_id = st.session_state.video_id

    st.markdown("<br>", unsafe_allow_html=True)

    stat1, stat2 = st.columns(2)

    with stat1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-name">Active video</div>
            <div class="stat-value">▶ &nbsp; {video_id}</div>
        </div>
        """, unsafe_allow_html=True)

    with stat2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-name">Knowledge chunks</div>
            <div class="stat-value">✳ &nbsp; {st.session_state.chunk_count} indexed</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("▶  Preview video", expanded=False):
        st.video(f"https://www.youtube.com/watch?v={video_id}")


    # -------------------- QUESTION INPUT --------------------

    st.markdown(
        '<div class="section-label">02 / ASK YOUR VIDEO</div>',
        unsafe_allow_html=True,
    )

    with st.form("question_form", clear_on_submit=False):
        question = st.text_area(
            "Your question",
            placeholder=(
                "What are the key ideas explained in this video?\n"
                "Ask about a concept, example, or explanation..."
            ),
            height=100,
        )

        ask_clicked = st.form_submit_button(
            "✦  Generate answer",
            type="primary",
            use_container_width=True,
        )

    if ask_clicked:
        if not question.strip():
            st.warning("Enter a question before generating an answer.")
        else:
            try:
                with st.spinner("Searching the transcript and crafting your answer..."):
                    result = answer_question(
                        st.session_state.vector_store,
                        question.strip(),
                    )

                st.session_state.last_result = result
                st.session_state.last_question = question.strip()

            except Exception as exc:
                st.error("Answer generation failed. Check your model and API limits.")
                with st.expander("Technical details"):
                    st.code(str(exc))


    # -------------------- ANSWER DISPLAY --------------------

    result = st.session_state.last_result

    if result is not None:
        st.markdown(
            '<div class="section-label">03 / YOUR ANSWER</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="answer-card">'
            f'<div class="answer-kicker">✳ &nbsp; AI-GENERATED RESPONSE</div>'
            f'<div class="answer-body">{""}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # Render answer as Markdown for readable formatting.
        st.markdown(result["answer"])

        sources = result.get("sources", [])
        has_evidence = result.get("has_evidence", bool(sources))

        if has_evidence and sources:
            st.markdown(
                '<div class="section-label">04 / SOURCE REFERENCES</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                '<p style="color:#929cb2;font-size:13px;">'
                'Explore the transcript passages used to support your answer.</p>',
                unsafe_allow_html=True,
            )

            for index, doc in enumerate(sources, start=1):
                seconds = int(doc.metadata.get("start_seconds", 0))
                timestamp = (
                    f"{seconds // 3600:02d}:"
                    f"{(seconds % 3600) // 60:02d}:"
                    f"{seconds % 60:02d}"
                )

                timestamp_url = (
                    f"https://www.youtube.com/watch?v={video_id}&t={seconds}s"
                )

                with st.expander(f"◈   Source {index}     ·     {timestamp}"):
                    st.markdown(
                        '<div style="color:#aeb7cb;font-size:13px;'
                        'line-height:1.9;">',
                        unsafe_allow_html=True,
                    )
                    st.write(doc.page_content)
                    st.markdown("</div>", unsafe_allow_html=True)

                    st.link_button(
                        "▶  Open at timestamp",
                        timestamp_url,
                    )


# -------------------- EMPTY STATE --------------------

else:
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="
        border:1px solid #282f43;
        border-radius:17px;
        padding:28px;
        background:linear-gradient(135deg,rgba(25,28,47,.9),rgba(15,19,30,.9));
    ">
        <div style="font-size:27px;margin-bottom:12px;">⌘</div>
        <div style="font-size:19px;font-weight:700;color:#edf0ff;margin-bottom:8px;">
            Your next video holds the answer.
        </div>
        <div style="color:#929cb2;font-size:14px;line-height:1.8;">
            Paste a YouTube link above to get started. Your transcript
            will be transformed into searchable chunks, ready for
            questions, grounded answers, and source exploration.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    a, b, c = st.columns(3)

    with a:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size:21px;">⌕</div>
            <div style="color:#e8eaf8;font-weight:700;margin:9px 0;">Ask naturally</div>
            <div style="color:#929cb2;font-size:12px;line-height:1.7;">
                Ask questions in your own words.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size:21px;">✳</div>
            <div style="color:#e8eaf8;font-weight:700;margin:9px 0;">Find meaning</div>
            <div style="color:#929cb2;font-size:12px;line-height:1.7;">
                Retrieve semantically relevant passages.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size:21px;">↗</div>
            <div style="color:#e8eaf8;font-weight:700;margin:9px 0;">Explore sources</div>
            <div style="color:#929cb2;font-size:12px;line-height:1.7;">
                Jump to supporting video timestamps.
            </div>
        </div>
        """, unsafe_allow_html=True)


# -------------------- FOOTER --------------------

st.markdown("""
<div class="footer">
    TRANSCRIPT AI &nbsp;·&nbsp; BUILT WITH PYTHON, LANGCHAIN, GEMINI & FAISS
    <br><br>
    Answers are generated from retrieved transcript evidence and may not always be correct.
</div>
""", unsafe_allow_html=True)
