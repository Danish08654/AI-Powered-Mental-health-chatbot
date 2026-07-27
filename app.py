import streamlit as st
import requests
import time

# Page config
st.set_page_config(
    page_title="Mental Health Support",
    page_icon="🌿",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&family=DM+Serif+Display&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #F0EDE6 !important;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }
.block-container { max-width: 760px !important; padding: 2rem 1.5rem 4rem !important; }

/* ── Hero ── */
.hero { text-align: center; padding: 2.5rem 0 1.5rem; }
.hero-icon {
    font-size: 2.8rem; display: block; margin-bottom: 0.6rem;
    animation: float 3s ease-in-out infinite;
}
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-6px)} }
.hero h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2.4rem; color: #1C3A2E;
    margin: 0 0 0.4rem; letter-spacing: -0.5px;
}
.hero p { font-size: 1rem; color: #5A7A6E; margin: 0; font-weight: 300; }

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(to right, transparent, #C8DDD5, transparent);
    margin: 1.5rem 0;
}

/* ── Chat bubbles ── */
.chat-area { display: flex; flex-direction: column; gap: 14px; min-height: 100px; margin-bottom: 1rem; }
.msg-row { display: flex; align-items: flex-end; gap: 10px; }
.msg-row.user { flex-direction: row-reverse; }
.avatar {
    width: 36px; height: 36px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; flex-shrink: 0;
}
.avatar.bot { background: #C8DDD5; }
.avatar.user-av { background: #D4C8E8; font-size: 0.75rem; font-weight: 600; color: #4A3878; }
.bubble { max-width: 74%; border-radius: 18px; padding: 12px 16px; font-size: 0.92rem; line-height: 1.65; }
.bubble.bot { background: #fff; border: 1px solid #E0EAE5; color: #1C3A2E; border-bottom-left-radius: 4px; }
.bubble.user-bubble { background: #2E6651; color: #fff; border-bottom-right-radius: 4px; }
.msg-time { font-size: 0.7rem; color: #9AB0A7; margin-top: 3px; padding: 0 4px; }
.msg-row.user .msg-time { text-align: right; }

/* ── Input ── */
.stTextInput > div > div > input {
    background: #fff !important; border: 1.5px solid #C8DDD5 !important;
    border-radius: 12px !important; padding: 14px 18px !important;
    font-size: 0.93rem !important; color: #1C3A2E !important;
    font-family: 'DM Sans', sans-serif !important; box-shadow: none !important;
}
.stTextInput > div > div > input:focus {
    border-color: #2E6651 !important;
    box-shadow: 0 0 0 3px rgba(46,102,81,0.12) !important;
}
.stTextInput > div > div > input::placeholder { color: #9AB0A7 !important; }

/* ── Buttons ── */
.stButton > button {
    background: #2E6651 !important; color: #fff !important;
    border: none !important; border-radius: 10px !important;
    padding: 10px 28px !important; font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important; font-weight: 500 !important;
    transition: background 0.15s !important; width: 100% !important;
}
.stButton > button:hover { background: #1C3A2E !important; }

/* ── Mood chips override ── */
div[data-testid="column"] .stButton > button {
    background: #fff !important; color: #2E6651 !important;
    border: 1.5px solid #C8DDD5 !important; border-radius: 24px !important;
    padding: 6px 10px !important; font-size: 0.78rem !important;
    font-weight: 400 !important;
}
div[data-testid="column"] .stButton > button:hover {
    background: #2E6651 !important; color: #fff !important; border-color: #2E6651 !important;
}

/* ── Crisis banner ── */
.crisis-bar {
    background: #FFF1F0; border: 1px solid #F5C4C4; border-radius: 10px;
    padding: 12px 16px; font-size: 0.82rem; color: #922020;
    margin: 1rem 0; display: flex; gap: 10px; align-items: flex-start;
}

/* ── Model badge ── */
.model-badge {
    display: inline-block;
    background: #E6F0EC; color: #1C3A2E;
    border-radius: 20px; padding: 3px 12px;
    font-size: 0.72rem; font-weight: 500;
    margin-bottom: 0.5rem;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] { background: #E8E3DA !important; }
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #1C3A2E !important; font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stSidebar"] .stButton > button {
    background: #fff !important; color: #922020 !important;
    border: 1px solid #F5C4C4 !important; border-radius: 8px !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #FFF1F0 !important;
}

/* ── Quick starter buttons ── */
.starter-btn .stButton > button {
    background: #fff !important; color: #2E6651 !important;
    border: 1px solid #C8DDD5 !important; border-radius: 10px !important;
    text-align: left !important; font-size: 0.85rem !important;
    padding: 10px 16px !important;
}
.starter-btn .stButton > button:hover {
    background: #E6F0EC !important; border-color: #2E6651 !important;
}

/* ── Footer ── */
.footer {
    text-align: center; font-size: 0.75rem; color: #9AB0A7;
    margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #D8E4DE;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# Load API key from st.secrets
# ─────────────────────────────────────────
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except (KeyError, FileNotFoundError):
    GROQ_API_KEY = None

# ─────────────────────────────────────────
# Models — best for empathetic / psychological conversation
# ─────────────────────────────────────────
MODELS = {
    "🧠 Llama 3.3 70B  (best quality)":   "llama-3.3-70b-versatile",
    "⚡ Llama 3.1 8B   (fastest)":         "llama-3.1-8b-instant",
    "🌀 DeepSeek R1 70B (reasoning)":      "deepseek-r1-distill-llama-70b",
    "💎 Llama 4 Maverick (multimodal)":    "meta-llama/llama-4-maverick-17b-128e-instruct",
    "🔮 Gemma 2 9B      (balanced)":       "gemma2-9b-it",
}

# ─────────────────────────────────────────
# System prompt  — tuned for mental health
# ─────────────────────────────────────────
SYSTEM_PROMPT = """You are MindEase, a compassionate and trauma-informed mental health support companion trained in active listening, cognitive-behavioural principles, and mindfulness-based techniques.

Core behaviour:
- Always validate and reflect feelings FIRST before any suggestion
- Keep replies warm, conversational, and concise (2–3 short paragraphs)
- Ask exactly ONE thoughtful follow-up question per reply
- Offer evidence-based coping tools (box breathing, 5-4-3-2-1 grounding, progressive muscle relaxation, journaling prompts, behavioural activation) when genuinely helpful
- Never diagnose, prescribe medication, or claim to replace a licensed therapist
- Acknowledge cultural differences in expressing distress without assumptions
- If the user mentions self-harm, suicidal thoughts, or a crisis, respond with care and compassion, take it seriously, and clearly provide: 988 Suicide & Crisis Lifeline (call/text 988, US), Crisis Text Line (text HOME to 741741), and International Association for Suicide Prevention directory at https://www.iasp.info/resources/Crisis_Centres/
- Use plain, warm language — never clinical jargon or bullet-point lists in your reply
- If the user seems to be a minor, be extra gentle and recommend involving a trusted adult"""

CRISIS_WORDS = [
    "suicide", "suicidal", "kill myself", "end my life", "self-harm", "self harm",
    "hurt myself", "don't want to live", "want to die", "not worth living",
    "cutting myself", "overdose", "no reason to live"
]

# ─────────────────────────────────────────
# Session state
# ─────────────────────────────────────────
for key, default in [("messages", []), ("show_crisis", False), ("msg_count", 0)]:
    if key not in st.session_state:
        st.session_state[key] = default

# ─────────────────────────────────────────
# Groq API call
# ─────────────────────────────────────────
def call_groq(messages, api_key, model, temp):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    # Groq uses "assistant" role; remap "bot" if any legacy key slipped through
    groq_msgs = []
    for m in messages:
        role = "assistant" if m["role"] in ("bot", "assistant") else "user"
        groq_msgs.append({"role": role, "content": m["content"]})
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + groq_msgs,
        "temperature": temp,
        "max_tokens": 700,
        "stream": False,
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

# ─────────────────────────────────────────
# Render chat history
# ─────────────────────────────────────────
def render_messages():
    html = '<div class="chat-area">'
    for msg in st.session_state.messages:
        t = time.strftime("%I:%M %p")
        content = msg["content"].replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
        if msg["role"] == "user":
            html += f"""
            <div class="msg-row user">
              <div class="avatar user-av">You</div>
              <div>
                <div class="bubble user-bubble">{content}</div>
                <div class="msg-time">{t}</div>
              </div>
            </div>"""
        else:
            html += f"""
            <div class="msg-row">
              <div class="avatar bot">🌿</div>
              <div>
                <div class="bubble bot">{content}</div>
                <div class="msg-time">{t}</div>
              </div>
            </div>"""
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# ─────────────────────────────────────────
# Hero
# ─────────────────────────────────────────
st.markdown("""
<div class="hero">
  <span class="hero-icon">🌿</span>
  <h1>MindEase</h1>
  <p>A safe, judgment-free space to share what you're carrying.</p>
</div>
""", unsafe_allow_html=True)

# Model badge
st.markdown(f'<div style="text-align:center"><span class="model-badge">✦ {model_label.split("(")[0].strip()}</span></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────
# Mood chips
# ─────────────────────────────────────────
moods = ["😔 Sad", "😰 Anxious", "😤 Frustrated", "🌊 Overwhelmed", "😶 Numb", "🌱 Hopeful"]
mood_cols = st.columns(len(moods))
selected_mood = None
for i, mood in enumerate(moods):
    with mood_cols[i]:
        if st.button(mood, key=f"mood_{i}", use_container_width=True):
            selected_mood = mood

# ─────────────────────────────────────────
# Crisis banner
# ─────────────────────────────────────────
if st.session_state.show_crisis:
    st.markdown("""
    <div class="crisis-bar">
      🆘 <span>If you're in crisis or having thoughts of self-harm, please reach out now.
      <strong>Call or text 988</strong> (US Suicide & Crisis Lifeline) ·
      Text <strong>HOME to 741741</strong> (Crisis Text Line) ·
      <a href="https://www.iasp.info/resources/Crisis_Centres/" target="_blank" style="color:#922020">International crisis centres</a>.
      You matter and support is available right now.</span>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# Chat area
# ─────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class="chat-area">
      <div class="msg-row">
        <div class="avatar bot">🌿</div>
        <div>
          <div class="bubble bot">
            Hi, I'm glad you're here. This is a safe space — no judgment, just listening.<br><br>
            Whatever you're feeling right now is valid. What's been on your mind lately?
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
else:
    render_messages()

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────
# Input area
# ─────────────────────────────────────────
col_input, col_btn = st.columns([5, 1])
with col_input:
    user_input = st.text_input(
        label="message", label_visibility="collapsed",
        placeholder="Share what's on your mind…", key="user_input"
    )
with col_btn:
    send = st.button("Send ↗")

# Mood chip triggers send
if selected_mood:
    user_input = f"I'm feeling {selected_mood} today"
    send = True

# ─────────────────────────────────────────
# Process message
# ─────────────────────────────────────────
def process_message(text):
    if not active_key:
        st.error("Please enter your Groq API key in the sidebar.")
        return

    if any(kw in text.lower() for kw in CRISIS_WORDS):
        st.session_state.show_crisis = True

    st.session_state.messages.append({"role": "user", "content": text})
    st.session_state.msg_count += 1

    with st.spinner("MindEase is listening…"):
        try:
            reply = call_groq(st.session_state.messages, active_key, model_id, temperature)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except requests.exceptions.HTTPError as e:
            st.session_state.messages.pop()
            code = e.response.status_code
            if code == 401:
                st.error("Invalid Groq API key — please check your key in the sidebar.")
            elif code == 429:
                st.error("Rate limit reached. Wait a moment and try again.")
            elif code == 404:
                st.error(f"Model '{model_id}' not found on your Groq plan. Try a different model.")
            else:
                st.error(f"API error {code}. Please try again.")
        except requests.exceptions.ConnectionError:
            st.session_state.messages.pop()
            st.error("Couldn't reach Groq. Check your internet connection.")
        except Exception as e:
            st.session_state.messages.pop()
            st.error(f"Something went wrong: {str(e)}")

    st.rerun()

if send and user_input and user_input.strip():
    process_message(user_input.strip())

# ─────────────────────────────────────────
# Quick starters (empty state only)
# ─────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("**Not sure where to start? Try one of these:**")
    starters = [
        "I've been feeling really anxious and can't slow my thoughts down",
        "I feel lonely and disconnected from the people around me",
        "I'm exhausted but can't sleep — stress keeps me up at night",
        "I want to learn some calming techniques for when I feel overwhelmed",
        "I've been feeling low and unmotivated for a while now",
    ]
    for s in starters:
        if st.button(f"💬  {s}", key=f"start_{s[:25]}"):
            process_message(s)

# ─────────────────────────────────────────
# Conversation depth nudge (every 8 turns)
# ─────────────────────────────────────────
if st.session_state.msg_count > 0 and st.session_state.msg_count % 8 == 0:
    st.info("💙 You've been sharing openly — that takes courage. If these feelings are persistent, speaking with a licensed therapist can offer deeper support.")

# ─────────────────────────────────────────
# Footer
# ─────────────────────────────────────────
st.markdown("""
<div class="footer">
  MindEase is not a substitute for professional mental health care. · For emergencies call 911. · Powered by Groq
</div>
""", unsafe_allow_html=True)
