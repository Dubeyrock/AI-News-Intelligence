import streamlit as st
from rag_pipeline import fetch_and_summarize, chat_with_news

# ─── Page Config ──────────────────────────────────────
st.set_page_config(
    page_title="SIGNAL — AI News Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Session State ────────────────────────────────────
for key, val in {
    "summary": None, "sources": [], "raw_articles": [],
    "news_context": None, "messages": [], "current_topic": "",
    "theme": "light"          # ← default: light
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ─── Theme Variables ──────────────────────────────────
is_dark = st.session_state.theme == "dark"

DARK = {
    "ink":              "#0c0c0e",
    "paper":            "#111116",
    "surface":          "#18181f",
    "border":           "rgba(255,255,255,0.07)",
    "muted":            "#42424f",
    "sub":              "#6e6e80",
    "body":             "#c9c9d4",
    "head":             "#f0f0f8",
    "gold":             "#d4a853",
    "gold_dim":         "rgba(212,168,83,0.12)",
    "gold_line":        "rgba(212,168,83,0.35)",
    "crimson":          "#c0392b",
    "sage":             "#4caf7d",
    "input_border":     "rgba(255,255,255,0.09)",
    "scrollbar_track":  "#0c0c0e",
    "scrollbar_thumb":  "#18181f",
    "masthead_rule":    "rgba(255,255,255,0.1)",
    "btn_color":        "#0c0c0e",
}

LIGHT = {
    "ink":              "#f5f0e8",
    "paper":            "#ede8dc",
    "surface":          "#e4ddd0",
    "border":           "rgba(0,0,0,0.08)",
    "muted":            "#a09888",
    "sub":              "#7a7060",
    "body":             "#3d3428",
    "head":             "#1a1209",
    "gold":             "#b5882a",
    "gold_dim":         "rgba(181,136,42,0.12)",
    "gold_line":        "rgba(181,136,42,0.4)",
    "crimson":          "#b52a1e",
    "sage":             "#2e7d52",
    "input_border":     "rgba(0,0,0,0.12)",
    "scrollbar_track":  "#f5f0e8",
    "scrollbar_thumb":  "#d4cdc0",
    "masthead_rule":    "rgba(0,0,0,0.12)",
    "btn_color":        "#f5f0e8",
}

T = DARK if is_dark else LIGHT

# ─── CSS ──────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {{
    --ink:        {T['ink']};
    --paper:      {T['paper']};
    --surface:    {T['surface']};
    --border:     {T['border']};
    --muted:      {T['muted']};
    --sub:        {T['sub']};
    --body:       {T['body']};
    --head:       {T['head']};
    --gold:       {T['gold']};
    --gold-dim:   {T['gold_dim']};
    --gold-line:  {T['gold_line']};
    --crimson:    {T['crimson']};
    --sage:       {T['sage']};
    --radius-sm:  8px;
    --radius-md:  14px;
}}

*, *::before, *::after {{ box-sizing: border-box; margin: 0; }}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {{
    font-family: 'DM Sans', sans-serif;
    background: var(--ink) !important;
    color: var(--body) !important;
}}

#MainMenu, footer, [data-testid="stToolbar"] {{ visibility: hidden; }}
[data-testid="stHeader"] {{ background: transparent !important; border-bottom: none !important; }}
.block-container {{ padding: 0 2rem 4rem !important; max-width: 1160px !important; }}

/* ══ SIDEBAR ══ */
[data-testid="stSidebar"] {{
    background: var(--paper) !important;
    border-right: 1px solid var(--border) !important;
}}
[data-testid="stSidebar"] .block-container {{ padding: 2rem 1.25rem !important; }}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown p {{
    color: var(--sub) !important;
    font-size: 0.82rem !important;
    font-family: 'DM Sans', sans-serif !important;
}}

.sb-logo {{
    display: flex; flex-direction: column; align-items: center; gap: 6px;
    padding-bottom: 1.75rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}}
.sb-wordmark {{
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem; font-weight: 900;
    color: var(--head); letter-spacing: 4px; text-transform: uppercase;
}}
.sb-tagline {{
    font-size: 0.62rem; font-weight: 500;
    letter-spacing: 3px; text-transform: uppercase; color: var(--gold);
}}
.sb-label {{
    font-size: 0.6rem; font-weight: 600;
    letter-spacing: 2.5px; text-transform: uppercase;
    color: var(--muted); margin: 1.5rem 0 0.6rem; display: block;
}}

.tech-grid {{
    display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 0.5rem;
}}
.tech-pill {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius-sm); padding: 6px 10px;
    font-size: 0.73rem; color: var(--sub); text-align: center;
    font-family: 'DM Mono', monospace;
}}
.sb-promo {{
    margin-top: 2rem; padding: 14px;
    border: 1px solid var(--gold-line);
    border-radius: var(--radius-md);
    background: var(--gold-dim); text-align: center;
}}
.sb-promo-name {{
    font-size: 0.65rem; font-weight: 700;
    letter-spacing: 2.5px; text-transform: uppercase; color: var(--gold);
}}
.sb-promo-sub {{ font-size: 0.72rem; color: var(--sub); margin-top: 3px; }}

/* ══ MASTHEAD ══ */
.masthead {{
    border-bottom: 3px double {T['masthead_rule']};
    padding: 2.5rem 0 1.5rem; margin-bottom: 2rem;
}}
.masthead-eyebrow {{ display: flex; align-items: center; gap: 10px; margin-bottom: 0.8rem; }}
.live-badge {{
    display: inline-flex; align-items: center; gap: 5px;
    background: var(--crimson); border-radius: 4px; padding: 3px 8px;
    font-size: 0.6rem; font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; color: #fff;
    font-family: 'DM Mono', monospace;
}}
.live-dot {{
    width: 6px; height: 6px; background: #fff; border-radius: 50%;
    animation: blink 1.2s step-start infinite;
}}
@keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
.issue-line {{ font-size: 0.72rem; color: var(--sub); font-family: 'DM Mono', monospace; letter-spacing: 1px; }}
.masthead-title {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(3rem, 6vw, 5.5rem); font-weight: 900;
    line-height: 1; color: var(--head); letter-spacing: -1px; margin-bottom: 0.4rem;
}}
.masthead-title span {{ color: var(--gold); font-style: italic; }}
.masthead-deck {{ font-size: 0.9rem; color: var(--sub); font-weight: 300; letter-spacing: 0.3px; }}
.rule-line {{
    border: none; height: 1px;
    background: linear-gradient(90deg, var(--gold) 0%, transparent 60%);
    margin: 1.5rem 0;
}}

/* ══ SEARCH ══ */
.search-label {{
    font-size: 0.65rem; font-weight: 600; letter-spacing: 3px;
    text-transform: uppercase; color: var(--muted); margin-bottom: 0.6rem;
    font-family: 'DM Mono', monospace;
}}
.stTextInput > div > div > input {{
    background: var(--surface) !important;
    border: 1px solid {T['input_border']} !important;
    border-radius: var(--radius-sm) !important;
    color: var(--head) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important; padding: 0.75rem 1.1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}}
.stTextInput > div > div > input:focus {{
    border-color: var(--gold-line) !important;
    box-shadow: 0 0 0 3px var(--gold-dim) !important;
    outline: none !important;
}}
.stTextInput > div > div > input::placeholder {{
    color: var(--muted) !important; font-style: italic;
}}

.stButton > button[kind="primary"] {{
    background: var(--gold) !important; border: none !important;
    border-radius: var(--radius-sm) !important;
    color: {T['btn_color']} !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important; font-size: 0.88rem !important;
    letter-spacing: 1px !important; text-transform: uppercase !important;
    padding: 0.75rem 1.4rem !important;
    transition: all 0.18s ease !important;
    box-shadow: 0 4px 20px var(--gold-dim) !important;
}}
.stButton > button[kind="primary"]:hover {{
    filter: brightness(1.1) !important;
    transform: translateY(-1px) !important;
}}
.stButton > button[kind="secondary"] {{
    background: transparent !important;
    border: 1px solid var(--border) !important;
    border-radius: 50px !important;
    color: var(--sub) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.8rem !important; font-weight: 400 !important;
    padding: 0.38rem 1rem !important;
    transition: all 0.18s ease !important;
}}
.stButton > button[kind="secondary"]:hover {{
    border-color: var(--gold-line) !important;
    color: var(--gold) !important;
    background: var(--gold-dim) !important;
}}

.topic-header {{
    font-size: 0.6rem; font-weight: 600; letter-spacing: 2.5px;
    text-transform: uppercase; color: var(--muted); margin: 1.4rem 0 0.7rem;
    font-family: 'DM Mono', monospace;
}}

/* ══ RESULTS ══ */
.result-header {{
    display: flex; align-items: baseline; gap: 14px;
    margin: 2rem 0 0.75rem; padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--border);
}}
.result-kicker {{
    font-size: 0.6rem; font-weight: 700; letter-spacing: 3px;
    text-transform: uppercase; color: var(--crimson); font-family: 'DM Mono', monospace;
}}
.result-topic {{ font-family: 'Playfair Display', serif; font-size: 1.35rem; font-weight: 700; color: var(--head); }}
.summary-body {{
    background: var(--paper);
    border: 1px solid var(--border);
    border-left: 3px solid var(--gold);
    border-radius: 0 var(--radius-md) var(--radius-md) 0;
    padding: 1.6rem 1.75rem; margin-bottom: 1.5rem;
    font-size: 0.92rem; line-height: 1.75; color: var(--body);
}}
.col-label {{
    font-size: 0.58rem; font-weight: 700; letter-spacing: 2.5px;
    text-transform: uppercase; color: var(--muted); margin-bottom: 0.75rem;
    font-family: 'DM Mono', monospace; display: block;
    border-bottom: 1px solid var(--border); padding-bottom: 6px;
}}
.source-row {{
    display: flex; align-items: center; gap: 10px;
    padding: 9px 12px; border-radius: var(--radius-sm);
    margin-bottom: 6px; border: 1px solid transparent;
    transition: all 0.18s ease; text-decoration: none !important;
    background: var(--surface);
}}
.source-row:hover {{ border-color: var(--gold-line); background: var(--gold-dim); }}
.source-idx {{ font-family: 'DM Mono', monospace; font-size: 0.65rem; color: var(--gold); min-width: 18px; }}
.source-txt {{ font-size: 0.76rem; color: var(--sub); word-break: break-all; }}
.article-row {{
    padding: 1rem 1.25rem; background: var(--surface);
    border: 1px solid var(--border); border-radius: var(--radius-sm);
    margin-bottom: 8px; transition: border-color 0.18s;
}}
.article-row:hover {{ border-color: var(--gold-line); }}
.article-num {{ font-family: 'DM Mono', monospace; font-size: 0.62rem; color: var(--gold); margin-bottom: 4px; letter-spacing: 1px; }}
.article-t {{ font-size: 0.86rem; font-weight: 600; color: var(--head); margin-bottom: 5px; line-height: 1.4; }}
.article-p {{ font-size: 0.77rem; color: var(--sub); line-height: 1.6; }}

/* ══ CHAT ══ */
.chat-masthead {{
    display: flex; align-items: center; gap: 12px;
    margin: 2.5rem 0 0.4rem; padding-top: 1.75rem;
    border-top: 1px solid var(--border);
}}
.chat-kicker {{
    font-size: 0.6rem; font-weight: 700; letter-spacing: 2.5px;
    text-transform: uppercase; color: var(--sage); font-family: 'DM Mono', monospace;
}}
.chat-hed {{ font-family: 'Playfair Display', serif; font-size: 1.2rem; font-weight: 700; color: var(--head); }}
.chat-dek {{ font-size: 0.8rem; color: var(--sub); margin-bottom: 1rem; }}
[data-testid="stChatMessage"] {{
    background: var(--surface) !important; border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important; padding: 0.75rem 1rem !important;
    margin-bottom: 0.55rem !important; font-family: 'DM Sans', sans-serif !important;
    color: var(--body) !important;
}}
[data-testid="stChatInput"] > div {{
    background: var(--surface) !important;
    border: 1px solid {T['input_border']} !important;
    border-radius: var(--radius-md) !important;
    font-family: 'DM Sans', sans-serif !important;
}}
[data-testid="stChatInput"] > div:focus-within {{ border-color: var(--gold-line) !important; }}

.streamlit-expanderHeader {{
    background: var(--surface) !important; border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important; color: var(--sub) !important;
    font-size: 0.83rem !important; font-family: 'DM Sans', sans-serif !important;
}}
.stSlider > div > div > div > div {{ background: var(--gold) !important; }}
.stSelectbox > div > div {{
    background: var(--surface) !important; border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important; color: var(--head) !important;
    font-family: 'DM Sans', sans-serif !important;
}}
.stAlert {{ border-radius: var(--radius-sm) !important; }}
.stSpinner > div {{ border-top-color: var(--gold) !important; }}
::-webkit-scrollbar {{ width: 5px; }}
::-webkit-scrollbar-track {{ background: {T['scrollbar_track']}; }}
::-webkit-scrollbar-thumb {{ background: {T['scrollbar_thumb']}; border-radius: 3px; }}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
        <div class="sb-wordmark">SIGNAL</div>
        <div class="sb-tagline">AI News Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Theme Toggle ──
    st.markdown('<span class="sb-label">🎨 Appearance</span>', unsafe_allow_html=True)
    switch_label = "Switch to 🌙 Dark" if not is_dark else "Switch to ☀️ Light"
    current_mode = "☀️ Light Mode" if not is_dark else "🌙 Dark Mode"
    st.markdown(
        f"<div style='font-size:0.78rem;color:var(--sub);margin-bottom:6px;"
        f"font-family:DM Mono,monospace;letter-spacing:1px;'>{current_mode}</div>",
        unsafe_allow_html=True
    )
    if st.button(switch_label, key="theme_toggle", use_container_width=True):
        st.session_state.theme = "dark" if not is_dark else "light"
        st.rerun()

    st.markdown('<span class="sb-label">⚙ Configuration</span>', unsafe_allow_html=True)
    max_results = st.slider("Articles to fetch", 3, 10, 5)

    st.markdown('<span class="sb-label">◈ Output Style</span>', unsafe_allow_html=True)
    format_style = st.selectbox(
        "format",
        ["Executive Summary", "Twitter Thread with Emojis", "5 Crisp Bullet Points", "Detailed Analysis"],
        label_visibility="collapsed"
    )

    st.markdown('<span class="sb-label">⬡ Tech Stack</span>', unsafe_allow_html=True)
    st.markdown("""
    <div class="tech-grid">
        <div class="tech-pill">Tavily</div>
        <div class="tech-pill">Groq</div>
        <div class="tech-pill">LangChain</div>
        <div class="tech-pill">Streamlit</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sb-promo">
        <div class="sb-promo-name">📺 CodeRebel</div>
        <div class="sb-promo-sub">Subscribe for more AI projects!</div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════
# MASTHEAD
# ═══════════════════════════════════
st.markdown("""
<div class="masthead">
    <div class="masthead-eyebrow">
        <span class="live-badge"><span class="live-dot"></span>LIVE</span>
        <span class="issue-line">RAG · GROQ · LANGCHAIN</span>
    </div>
    <div class="masthead-title">Real‑Time <span>Intelligence</span></div>
    <div class="masthead-deck">Your AI‑powered editorial desk — fetching, analysing & contextualising news as it breaks.</div>
    <hr class="rule-line">
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════
# SEARCH
# ═══════════════════════════════════
st.markdown('<div class="search-label">↳ Enter a topic to investigate</div>', unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])
with col1:
    topic = st.text_input(
        "topic_input",
        placeholder="e.g.  AI breakthroughs · India economy · SpaceX launch · Budget 2026",
        label_visibility="collapsed"
    )
with col2:
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    search_btn = st.button("Analyse →", type="primary", use_container_width=True)

st.markdown('<div class="topic-header">⚡ Quick Beats</div>', unsafe_allow_html=True)
q_cols = st.columns(6)
quick_topics = ["🤖 AI News", "🇮🇳 India Tech", "🌍 Climate", "📈 Stock Market", "🚀 Space", "💊 Health"]
for i, qt in enumerate(quick_topics):
    if q_cols[i].button(qt, key=f"qt_{i}"):
        topic = qt.split(" ", 1)[1]
        search_btn = True

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)


# ═══════════════════════════════════
# FETCH LOGIC
# ═══════════════════════════════════
if search_btn:
    if topic:
        clean_topic = topic.lstrip("🤖🇮🇳🌍📈🚀💊 ")
        with st.spinner(f"Investigating **{clean_topic}** across live sources…"):
            try:
                result = fetch_and_summarize(clean_topic, format_style=format_style)
                st.session_state.summary       = result["summary"]
                st.session_state.sources       = result["sources"]
                st.session_state.raw_articles  = result["raw_articles"]
                st.session_state.current_topic = clean_topic
                st.session_state.messages      = []

                ctx = ""
                for idx, a in enumerate(result["raw_articles"]):
                    ctx += f"[Article {idx+1}]\nTitle: {a.get('title')}\nContent: {a.get('content')}\n\n"
                st.session_state.news_context = ctx

            except Exception as e:
                st.error(f"⚠  {str(e)}")
                st.info("Check your API keys in the .env file")
    else:
        st.warning("Please enter a topic to investigate.")


# ═══════════════════════════════════
# RESULTS
# ═══════════════════════════════════
if st.session_state.summary:

    st.markdown(f"""
    <div class="result-header">
        <span class="result-kicker">AI Analysis</span>
        <span class="result-topic">{st.session_state.current_topic}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="summary-body">', unsafe_allow_html=True)
    st.markdown(st.session_state.summary)
    st.markdown("</div>", unsafe_allow_html=True)

    left, right = st.columns([1, 1])

    with left:
        st.markdown('<span class="col-label">⬡ Source Index</span>', unsafe_allow_html=True)
        for i, url in enumerate(st.session_state.sources):
            if url:
                short = url.replace("https://", "").replace("http://", "")[:58]
                st.markdown(f"""
                <a href="{url}" target="_blank" class="source-row">
                    <span class="source-idx">#{i+1:02d}</span>
                    <span class="source-txt">{short}…</span>
                </a>
                """, unsafe_allow_html=True)

    with right:
        with st.expander("↗  Raw Article Feed", expanded=False):
            for i, article in enumerate(st.session_state.raw_articles):
                title   = article.get("title", "Untitled")
                preview = article.get("content", "")[:300]
                st.markdown(f"""
                <div class="article-row">
                    <div class="article-num">ARTICLE {i+1:02d}</div>
                    <div class="article-t">{title}</div>
                    <div class="article-p">{preview}…</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="chat-masthead">
        <div>
            <div class="chat-kicker">● On the Record</div>
            <div class="chat-hed">Chat with the Newsroom</div>
        </div>
    </div>
    <div class="chat-dek">Ask follow‑up questions grounded in live data about <strong style="color:var(--gold)">{st.session_state.current_topic}</strong></div>
    """, unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask anything about the news…"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Analysing…"):
                response = chat_with_news(
                    prompt,
                    st.session_state.news_context,
                    st.session_state.messages[:-1]
                )
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})