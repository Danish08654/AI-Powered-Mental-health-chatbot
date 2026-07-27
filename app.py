import streamlit as st
import requests
import time

st.set_page_config(
    page_title="MindEase",
    page_icon="🌿",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&family=DM+Serif+Display&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #F0EDE6 !important;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stDecoration"] { display: none; }
.block-container { max-width: 740px !important; padding: 2rem 1.5rem 4rem !important; }

/* Hero */
.hero { text-align: center; padding: 2rem 0 1rem; }
.hero-leaf { font-size: 2.2rem; display: block; margin-bottom: 0.5rem; animation: float 3s ease-in-out infinite; }
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-5px)} }
.hero h1 { font-family: 'DM Serif Display', serif; font-size: 2.2rem; color: #1C3A2E; margin: 0 0 0.3rem; letter-spacing: -0.5px; }
.hero p { font-size: 0.95rem; color: #5A7A6E; margin: 0; font-weight: 300; }

/* Divider */
.divider { height: 1px; background: linear-gradient(to right, transparent, #C8DDD5, transparent); margin: 1.2rem 0; }

/* Chat */
.chat-area { display: flex; flex-direction: column; gap: 12px; margin-bottom: 1rem; }
.msg-row { display: flex; align-items: flex-end; gap: 9px; }
.msg-row.user { flex-direction: row-reverse; }
.avatar { width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-size: 0.85rem; }
.avatar.bot { background: #C8DDD5; font-size: 1rem; }
.avatar.user-av { background: #D4C8E8; font-weight: 600; color: #4A3878; font-size: 0.7rem; }
.bubble { max-width: 72%; border-radius: 16px; padding: 11px 15px; font-size: 0.91rem; line-height: 1.65; }
.bubble.bot { background: #fff; border: 1px solid #E0EAE5; color: #1C3A2E; border-bottom-left-radius: 3px; }
.bubble.user-bubble { background: #2E6651; color: #fff; border-bottom-right-radius: 3px; }
.msg-time { font-size: 0.68rem; color: #9AB0A7; margin-top: 2px; padding: 0 3px; }
.msg-row.user .msg-time { text-align: right; }

/* Mood chips — column buttons */
div[data-testid="column"] .stButton > button {
    background: #fff !important; color: #2E6651 !important;
    border: 1px solid #C8DDD5 !important; border-radius: 20px !important;
    padding: 5px 8px !important; font-size: 0.76rem !important;
    font-weight: 400 !important; width: 100% !important;
}
div[data-testid="column"] .stButton > button:hover {
    background: #2E6651 !important; color: #fff !important; border-color: #2E6651 !important;
}

/* Send button */
.stButton > button {
    background: #2E6651 !important; color: #fff !important;
    border: none !important; border-radius: 10px !important;
    padding: 10px 20px !important; font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important; font-weight: 500 !important; width: 100% !important;
}
.stButton > button:hover { background: #1C3A2E !important; }

/* Input */
.stTextInput > div > div > input {
    background: #fff !important; border: 1px solid #C8DDD5 !important;
    border-radius: 10px !important; padding: 12px 16px !important;
    font-size: 0.92rem !important; color: #1C3A2E !important;
    font-family: 'DM Sans', sans-serif !important; box-shadow: none !important;
}
.stTextInput > div > div > input:focus { border-color: #2E6651 !important; box-shadow: 0 0 0 2px rgba(46,102,81,0.1) !important; }
.stTextInput > div > div > input::placeholder { color: #B0C4BB !important; }

/* Crisis */
.crisis-bar {
    background: #FFF1F0; border: 1px solid #F5C4C4; border-radius: 8px;
    padding: 10px 14px; font-size: 0.81rem; color: #922020; margin: 0.8rem 0;
}

/* Sidebar — minimal */
[data-testid="stSidebar"] { background: #EAE6DF !important; }
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h3 { color: #1C3A2E !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.88rem !important; }
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important; color: #7A3030 !important;
    border: 1px solid #E8C4C4 !important; border-radius: 7px !important;
    font-size: 0.83rem !important;
}
[data-testid="stSidebar"] .stButton > button:hover { background: #FFF1F0 !important; }

/* Starters */
.starter-wrap .stButton > button {
    background: #fff !important; color: #2E6651 !important;
    border: 1px solid #D8E8E2 !important; border-radius: 8px !important;
    text-align: left !important; font-size: 0.84rem !important;
    padding: 9px 14px !important; font-weight: 400 !important;
}
.starter-wrap .stButton > button:hover { background: #EAF3EE !important; border-color: #2E6651 !important; }

/* Footer */
.footer { text-align: center; font-size: 0.72rem; color: #B0C4BB; margin-top: 1.5rem; padding-top: 0.8rem; border-top: 1px solid #DDE8E3; }
</style>
""", unsafe_allow_html=True)

# ── API key from secrets ──
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except (KeyError, FileNotFoundError):
    GROQ_API_KEY = None

MODELS = {
    "Llama 3.3 70B":        "llama-3.3-70b-versatile",
    "Llama 3.1 8B (fast)":  "llama-3.1-8b-instant",
    "DeepSeek R1 70B":      "deepseek-r1-distill-llama-70b",
    "Gemma 2 9B":           "gemma2-9b-it",
}

SYSTEM_PROMPT = """You are MindEase, a compassionate and trauma-informed mental health support companion.

Core behaviour:
- Validate and reflect the user's feelings first, before anything else
- Be warm, concise, and conversational — 2 to 3 short paragraphs maximum
- Ask exactly one thoughtful follow-up question per reply
- Offer evidence-based coping tools (box breathing, 5-4-3-2-1 grounding, journaling, progressive muscle relaxation) only when genuinely relevant
- Never diagnose, prescribe, or claim to replace a licensed therapist
- If the user mentions self-harm or suicidal thoughts, respond with care and provide: 988 Suicide & Crisis Lifeline (call or text 988), Crisis Text Line (text HOME to 741741)
- Write in plain, warm prose — no bullet points, no clinical language, no lists"""

CRISIS_WORDS = [
    "suicide", "suicidal", "kill myself", "end my life", "self-harm", "self harm",
    "hurt myself", "don't want to live", "want to die", "not worth living",
    "cutting myself", "overdose", "no reason to live"
]

for k, v in [("messages", []), ("show_crisis", False)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar ──
with st.sidebar:
    st.markdown("### Settings")

    if GROQ_API_KEY:
        st.success("API key loaded")
        active_key = GROQ_API_KEY
    else:
        manual_key = st.text_input("Groq API Key", type="password", placeholder="gsk_…")
        active_key = manual_key or None
        if not active_key:
            st.caption("Enter your key to start. Get one free at console.groq.com")

    model_label = st.selectbox("Model", list(MODELS.keys()), index=0)
    model_id = MODELS[model_label]

    temperature = st.slider("Warmth", 0.3, 1.0, 0.72, 0.05)

    st.markdown("---")
    st.markdown("**Crisis lines**")
    st.caption("988 — Suicide & Crisis Lifeline\n\n741741 — Crisis Text Line (text HOME)\n\n911 — Emergencies")
    st.markdown("---")
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.session_state.show_crisis = False
        st.rerun()

# ── Groq call ──
def call_groq(messages, api_key, model, temp):
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    groq_msgs = [
        {"role": "assistant" if m["role"] == "assistant" else "user", "content": m["content"]}
        for m in messages
    ]
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + groq_msgs,
        "temperature": temp,
        "max_tokens": 600,
    }
    resp = requests.post("https://api.groq.com/openai/v1/chat/completions",
                         headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

# ── Render messages ──
def render_messages():
    html = '<div class="chat-area">'
    for msg in st.session_state.messages:
        t = time.strftime("%I:%M %p")
        c = msg["content"].replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
        if msg["role"] == "user":
            html += f'<div class="msg-row user"><div class="avatar user-av">You</div><div><div class="bubble user-bubble">{c}</div><div class="msg-time">{t}</div></div></div>'
        else:
            html += f'<div class="msg-row"><div class="avatar bot">🌿</div><div><div class="bubble bot">{c}</div><div class="msg-time">{t}</div></div></div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# ── Process message ──
def process_message(text):
    if not active_key:
        st.error("Enter your Groq API key in the sidebar.")
        return
    if any(kw in text.lower() for kw in CRISIS_WORDS):
        st.session_state.show_crisis = True
    st.session_state.messages.append({"role": "user", "content": text})
    with st.spinner(""):
        try:
            reply = call_groq(st.session_state.messages, active_key, model_id, temperature)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except requests.exceptions.HTTPError as e:
            st.session_state.messages.pop()
            code = e.response.status_code
            msgs = {401: "Invalid API key.", 429: "Rate limit hit — wait a moment.", 404: f"Model '{model_id}' unavailable on your plan."}
            st.error(msgs.get(code, f"API error {code}."))
        except Exception as e:
            st.session_state.messages.pop()
            st.error(f"Something went wrong: {e}")
    st.rerun()

# ── Hero ──
st.markdown("""
<div class="hero">
  <span class="hero-leaf">🌿</span>
  <h1>MindEase</h1>
  <p>A safe, judgment-free space to share what you're carrying.</p>
</div>
""", unsafe_allow_html=True)


# ── Chat area ──
if not st.session_state.messages:
    st.markdown("""<div class="chat-area">
      <div class="msg-row">
        <div class="avatar bot">🌿</div>
        <div>
          <div class="bubble bot">
            Hi, I'm glad you're here. This is a safe space — no judgment, just listening.<br><br>
            Whatever you're feeling right now is valid. What's been on your mind lately?
          </div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)
else:
    render_messages()

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Input ──
col_input, col_btn = st.columns([5, 1])
with col_input:
    user_input = st.text_input("message", label_visibility="collapsed",
                               placeholder="Share what's on your mind…", key="user_input")
with col_btn:
    send = st.button("Send")

if send and user_input and user_input.strip():
    process_message(user_input.strip())
