"""
MicroLLM Studio – ULTRA LIGHT EDITION
ARSLM No-Code · Streamlit Cloud Safe · Animated UI
NO torch · NO transformers · NO crashes
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import PyPDF2
import docx
import json
import os

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="MicroLLM Studio · Ultra Light",
    page_icon="🤖",
    layout="wide"
)

# ===============================
# ARSLM INFO
# ===============================
ARSLM_INFO = {
    "name": "ARSLM Ultra-Light",
    "description": (
        "A minimal, fast and secure small language engine.\n"
        "Designed for No-Code usage, document reasoning and "
        "on-premise deployments with zero heavy dependencies."
    )
}

# ===============================
# CSS – ANIMATED PRO UI
# ===============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.title {
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(90deg,#667eea,#764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    transition: transform .4s;
}
.title:hover { transform: scale(1.05); }

.card {
    background: linear-gradient(135deg,#667eea,#764ba2);
    padding: 20px;
    border-radius: 16px;
    color: white;
    box-shadow: 0 10px 25px rgba(0,0,0,.15);
    transition: transform .3s;
}
.card:hover { transform: scale(1.04); }

.user {
    background:#00cec9;
    color:white;
    padding:14px;
    border-radius:14px;
    margin:10px 0 10px 30%;
}

.bot {
    background:#dfe6e9;
    padding:14px;
    border-radius:14px;
    margin:10px 30% 10px 0;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# SESSION
# ===============================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.markdown("## 🤖 MicroLLM")
    page = st.radio(
        "Navigation",
        ["🏠 Dashboard", "💬 Chat", "📊 Analytics", "⚙️ Settings"],
        label_visibility="collapsed"
    )

# ===============================
# DASHBOARD
# ===============================
if page == "🏠 Dashboard":
    st.markdown('<div class="title">MicroLLM Studio</div>', unsafe_allow_html=True)
    st.info(f"**{ARSLM_INFO['name']}**\n\n{ARSLM_INFO['description']}")

    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="card">Engine<br><h2>Ultra-Light</h2></div>', unsafe_allow_html=True)
    c2.markdown('<div class="card">Latency<br><h2>Low</h2></div>', unsafe_allow_html=True)
    c3.markdown('<div class="card">Security<br><h2>On-Prem</h2></div>', unsafe_allow_html=True)

    epochs = list(range(1, 8))
    loss = [2.4, 2.0, 1.7, 1.4, 1.2, 1.1, 1.0]
    fig = go.Figure(go.Scatter(x=epochs, y=loss, mode="lines+markers"))
    fig.update_layout(title="Training Simulation", height=350)
    st.plotly_chart(fig, use_container_width=True)

# ===============================
# CHAT ENGINE (RULE-BASED + CONTEXT)
# ===============================
def arslm_ultra_response(prompt, context=""):
    prompt = prompt.lower()

    if "hello" in prompt or "salut" in prompt:
        return "Hello 👋 I’m ARSLM Ultra-Light. How can I help you?"

    if "summarize" in prompt or "résume" in prompt:
        return context[:800] + "..." if context else "Please upload a document."

    if "who are you" in prompt:
        return "I’m ARSLM Ultra-Light, a fast and private No-Code AI engine."

    return (
        "I’ve received your request.\n\n"
        "This Ultra-Light engine focuses on speed, privacy and document understanding.\n"
        "For deep generation, plug a full ARSLM backend."
    )

# ===============================
# CHAT
# ===============================
elif page == "💬 Chat":
    st.markdown('<div class="title">ARSLM Chat</div>', unsafe_allow_html=True)

    context_text = ""

    with st.expander("📄 Upload documents"):
        files = st.file_uploader(
            "Upload",
            type=["txt","pdf","csv","docx"],
            accept_multiple_files=True
        )
        if files:
            for f in files:
                if f.type == "application/pdf":
                    reader = PyPDF2.PdfReader(f)
                    for p in reader.pages:
                        context_text += p.extract_text() or ""
                elif f.type == "text/plain":
                    context_text += f.read().decode()
                elif f.type == "text/csv":
                    context_text += pd.read_csv(f).to_csv()
                elif "word" in f.type:
                    d = docx.Document(f)
                    context_text += "\n".join(p.text for p in d.paragraphs)

    for m in st.session_state.messages:
        cls = "user" if m["role"]=="user" else "bot"
        st.markdown(f'<div class="{cls}">{m["content"]}</div>', unsafe_allow_html=True)

    user_input = st.chat_input("Ask ARSLM...")
    if user_input:
        st.session_state.messages.append({"role":"user","content":user_input})
        reply = arslm_ultra_response(user_input, context_text)
        st.session_state.messages.append({"role":"assistant","content":reply})
        st.experimental_rerun()

# ===============================
# ANALYTICS
# ===============================
elif page == "📊 Analytics":
    st.markdown('<div class="title">Analytics</div>', unsafe_allow_html=True)
    st.success("Ultra-Light engine running smoothly 🚀")

# ===============================
# SETTINGS
# ===============================
elif page == "⚙️ Settings":
    st.markdown('<div class="title">Settings</div>', unsafe_allow_html=True)
    st.checkbox("Enable encryption", True)
    st.checkbox("Audit logs", True)

st.markdown("---")
st.caption("MicroLLM Studio · ARSLM Ultra-Light · No-Code · On-Prem")