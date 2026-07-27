import streamlit as st
import requests
import json
import time

# ─────────────────────────────────────────
# Page config
# ─────────────────────────────────────────
st.set_page_config(
    page_title="MindEase – Mental Health Support",
    page_icon="🌿",
    layout="centered"
)

# ─────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap');

/* ── Reset & base ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #F0EDE6 !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }
.block-container { max-width: 760px !important; padding: 2rem 1.5rem 4rem !important; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
}
.hero-icon {
    font-size: 2.8rem;
    display: block;
    margin-bottom: 0.6rem;
    animation: float 3s ease-in-out infinite;
}
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-6px)} }

.hero h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2.4rem;
    color: #1C3A2E;
    margin: 0 0 0.4rem;
    letter-spacing: -0.5px;
}
.hero p {
    font-size: 1rem;
    color: #5A7A6E;
    margin: 0;
    font-weight: 300;
}

/* ── Mood chips ── */
.mood-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin: 1.2rem 0 0.5rem;
}
.mood-chip {
    background: #fff;
    border: 1.5px solid #C8DDD5;
    border-radius: 24px;
    padding: 6px 16px;
    font-size: 0.82rem;
    color: #2E6651;
    cursor: pointer;
    transition: all 0.15s;
    font-family: 'DM Sans', sans-serif;
}
.mood-chip:hover {
    background: #2E6651;
    color: #fff;
    border-color: #2E6651;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(to right, transparent, #C8DDD5, transparent);
    margin: 1.5rem 0;
}

/* ── Chat bubbles ── */
.chat-area {
    display: flex;
    flex-direction: column;
    gap: 14px;
    min-height: 100px;
    margin-bottom: 1rem;
}

.msg-row {
    display: flex;
    align-items: flex-end;
    gap: 10px;
}
.msg-row.user { flex-direction: row-reverse; }

.avatar {
    width: 36px; height: 36px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}
.avatar.bot { background: #C8DDD5; }
.avatar.user-av { background: #D4C8E8; font-size: 0.75rem; font-weight: 600; color: #4A3878; }

.bubble {
    max-width: 74%;
    border-radius: 18px;
    padding: 12px 16px;
    font-size: 0.92rem;
    line-height: 1.65;
}
.bubble.bot {
    background: #fff;
    border: 1px solid #E0EAE5;
    color: #1C3A2E;
    border-bottom-left-radius: 4px;
}
.bubble.user-bubble {
    background: #2E6651;
    color: #fff;
    border-bottom-right-radius: 4px;
}

.msg-time {
    font-size: 0.7rem;
    color: #9AB0A7;
    margin-top: 3px;
    padding: 0 4px;
}
.msg-row.user .msg-time { text-align: right; }

/* ── Typing dots ── */
.typing-dots {
    display: inline-flex;
    gap: 5px;
    align-items: center;
    padding: 12px 16px;
    background: #fff;
    border: 1px solid #E0EAE5;
    border-radius: 18px;
    border-bottom-left-radius: 4px;
}
.dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #9AB0A7;
    animation: bounce 1.3s infinite;
}
.dot:nth-child(2){animation-delay:.2s}
.dot:nth-child(3){animation-delay:.4s}
@keyframes bounce{0%,80%,100%{transform:translateY(0)}40%{transform:translateY(-7px)}}

/* ── Input styling ── */
.stTextInput > div > div > input {
    background: #fff !important;
    border: 1.5px solid #C8DDD5 !important;
    border-radius: 12px !important;
    padding: 14px 18px !important;
    font-size: 0.93rem !important;
    color: #1C3A2E !important;
    font-family: 'DM Sans', sans-serif !important;
    box-shadow: none !important;
}
.stTextInput > div > div > input:focus {
    border-color: #2E6651 !important;
    box-shadow: 0 0 0 3px rgba(46,102,81,0.12) !important;
}
.stTextInput > div > div > input::placeholder { color: #9AB0A7 !important; }

/* ── Buttons ── */
.stButton > button {
    background: #2E6651 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 28px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    transition: background 0.15s !important;
    width: 100% !important;
}
.stButton > button:hover { background: #1C3A2E !important; }

/* ── Crisis banner ── */
.crisis-bar {
    background: #FFF1F0;
    border: 1px solid #F5C4C4;
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 0.82rem;
    color: #922020;
    margin: 1rem 0;
    display: flex;
    gap: 10px;
    align-items: flex-start;
}

/* ── API key box ── */
.stTextInput[data-testid="api-key"] > div > div > input {
    letter-spacing: 3px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #E8E3DA !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #1C3A2E !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Footer ── */
.footer {
    text-align: center;
    font-size: 0.75rem;
    color: #9AB0A7;
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid #D8E4DE;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# System prompt
# ─────────────────────────────────────────
SYSTEM_PROMPT = """You are MindEase, a compassionate mental health support companion. Your role:
- Listen actively and validate feelings before offering suggestions
- Respond with warmth, empathy, and genuine care (2-3 short paragraphs max)
- Ask one thoughtful follow-up question per response
- Offer gentle coping strategies (breathing, grounding, journaling) when appropriate
- Never diagnose, prescribe, or replace professional therapy
- If someone expresses thoughts of self-harm or suicide, respond with care and strongly encourage calling 988 (US Suicide & Crisis Lifeline)
- Use conversational, plain language — never clinical jargon
- Always reflect feelings back before suggesting anything"""

CRISIS_WORDS = ["suicide", "kill myself", "end my life", "self-harm",
                "hurt myself", "don't want to live", "want to die", "not worth living"]

# ─────────────────────────────────────────
# Session state
# ─────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_crisis" not in st.session_state:
    st.session_state.show_crisis = False

# ─────────────────────────────────────────
# Sidebar – settings
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    groq_key = st.text_input("Groq API Key", type="password",
                             placeholder="gsk_…",
                             help="Get a free key at console.groq.com")
    
    model_choice = st.selectbox("Model", [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768",
        "gemma2-9b-it",
    ], index=0)

    temperature = st.slider("Response warmth", 0.3, 1.0, 0.75, 0.05,
                            help="Higher = more expressive responses")

    st.markdown("---")
    st.markdown("### 🆘 Crisis Resources")
    st.markdown("""
- **988** – Suicide & Crisis Lifeline  
- **741741** – Crisis Text Line  
- **911** – Emergencies  
    """)
    st.markdown("---")
    if st.button("🗑 Clear chat"):
        st.session_state.messages = []
        st.session_state.show_crisis = False
        st.rerun()

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

# ─────────────────────────────────────────
# Mood chips (inject via st.button columns)
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
      <strong>Call or text 988</strong> (US) · Text HOME to <strong>741741</strong> (Crisis Text Line).
      You matter and help is available.</span>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# Groq API call
# ─────────────────────────────────────────
def call_groq(messages, api_key, model, temp):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        "temperature": temp,
        "max_tokens": 600,
        "stream": False
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
        if msg["role"] == "user":
            html += f"""
            <div class="msg-row user">
              <div class="avatar user-av">You</div>
              <div>
                <div class="bubble user-bubble">{msg['content']}</div>
                <div class="msg-time">{t}</div>
              </div>
            </div>"""
        else:
            html += f"""
            <div class="msg-row">
              <div class="avatar bot">🌿</div>
              <div>
                <div class="bubble bot">{msg['content'].replace(chr(10), '<br>')}</div>
                <div class="msg-time">{t}</div>
              </div>
            </div>"""
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# ─────────────────────────────────────────
# Welcome message
# ─────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class="chat-area">
      <div class="msg-row">
        <div class="avatar bot">🌿</div>
        <div>
          <div class="bubble bot">
            Hi, I'm glad you're here. This is a safe space — no judgment, just listening.<br><br>
            What's been on your mind lately?
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
        label="message",
        label_visibility="collapsed",
        placeholder="Share what's on your mind…",
        key="user_input"
    )
with col_btn:
    send = st.button("Send ↗")

# Handle mood chip selection
if selected_mood:
    user_input = f"I'm feeling {selected_mood} today"
    send = True

# ─────────────────────────────────────────
# Process send
# ─────────────────────────────────────────
if send and user_input and user_input.strip():
    text = user_input.strip()

    # Check for API key
    if not groq_key:
        st.error("Please enter your Groq API key in the sidebar to start chatting.")
        st.stop()

    # Check crisis keywords
    if any(kw in text.lower() for kw in CRISIS_WORDS):
        st.session_state.show_crisis = True

    # Save user message
    st.session_state.messages.append({"role": "user", "content": text})

    # Call Groq
    with st.spinner("MindEase is listening…"):
        try:
            reply = call_groq(
                [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                groq_key, model_choice, temperature
            )
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                st.error("Invalid Groq API key. Please check your key in the sidebar.")
            else:
                st.error(f"API error: {e.response.status_code}. Please try again.")
            st.session_state.messages.pop()  # remove unresponded user message
        except requests.exceptions.ConnectionError:
            st.error("Couldn't connect to Groq. Check your internet connection.")
            st.session_state.messages.pop()
        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")
            st.session_state.messages.pop()

    st.rerun()

# ─────────────────────────────────────────
# Quick starters (show only at start)
# ─────────────────────────────────────────
if len(st.session_state.messages) == 0:
    st.markdown("**Try saying:**")
    starters = [
        "I've been feeling anxious and can't slow my thoughts down",
        "I feel really lonely lately",
        "I'm struggling to sleep because of stress",
        "I need some calming techniques",
    ]
    for s in starters:
        if st.button(f"💬 {s}", key=f"start_{s[:20]}"):
            st.session_state.messages.append({"role": "user", "content": s})
            if groq_key:
                with st.spinner("MindEase is listening…"):
                    try:
                        reply = call_groq(
                            [{"role": "user", "content": s}],
                            groq_key, model_choice, temperature
                        )
                        st.session_state.messages.append({"role": "assistant", "content": reply})
                    except Exception:
                        st.session_state.messages.pop()
            st.rerun()

# ─────────────────────────────────────────
# Footer
# ─────────────────────────────────────────
st.markdown("""
<div class="footer">
  MindEase is not a substitute for professional mental health care. 
  For emergencies, call 911. · Powered by Groq
</div>
""", unsafe_allow_html=True)
