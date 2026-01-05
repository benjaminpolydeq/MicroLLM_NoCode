"""
MicroLLM Studio - Ultra-Light Streamlit Assistant IA
No-Code, Local, Multilingue (FR/EN/ES)
Supports: TXT, PDF, DOCX, CSV, Code
"""

import streamlit as st
from datetime import datetime
import PyPDF2
import docx
import pandas as pd
import time

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="MicroLLM Studio",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# CSS ANIMATIONS
# ===============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }

.main-header {
    font-size: 2.5rem; font-weight: bold; 
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}
.main-header:hover { transform: scale(1.05); }

.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white; padding: 15px; border-radius: 12px; text-align:center;
    box-shadow:0 4px 10px rgba(0,0,0,0.2); transition: transform 0.3s;
    cursor:pointer; margin: 5px;
}
.metric-card:hover { transform: scale(1.05); }

.user-msg { background: #81ecec; color:#2d3436; padding:10px; border-radius:12px; margin-left:25%; margin-bottom:5px; }
.assistant-msg { background: #dfe6e9; color:#2d3436; padding:10px; border-radius:12px; margin-right:25%; margin-bottom:5px; }

.stButton button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color:white; border:none; padding:8px 16px; border-radius:8px; font-weight:600; transition: all 0.3s ease; }
.stButton button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(102,126,234,0.4); }
</style>
""", unsafe_allow_html=True)

# ===============================
# SESSION STATE
# ===============================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ===============================
# MULTILINGUE SIMPLE
# ===============================
LANG_MAP = {"fr": "fr", "en": "en", "es": "es"}

def translate_text(text, target="en"):
    # Ultra-light: juste retour texte si target != en
    if target not in LANG_MAP: return text
    return f"[{target.upper()}] {text}"

# ===============================
# ARSLM Ultra-Light Engine
# ===============================
class ARSLMEngine:
    def __init__(self):
        self.knowledge_base = [
            {"keywords": ["code", "algorithm", "function"], "response": "Vous pouvez analyser et résumer des fonctions et algorithmes."},
            {"keywords": ["data", "database"], "response": "Je peux traiter et résumer vos bases de données locales."},
            {"keywords": ["legal", "juridique"], "response": "Analyse juridique et recherche sur documents disponibles."},
            {"keywords": ["medical", "santé"], "response": "Résumé et traitement des textes scientifiques et médicaux."},
            {"keywords": ["research", "scientific"], "response": "Assistant scientifique pour recherches locales approfondies."},
        ]
        self.history = []

    def generate_response(self, query):
        query_low = query.lower()
        best = None
        score = 0
        for item in self.knowledge_base:
            s = sum(1 for kw in item["keywords"] if kw in query_low)
            if s > score:
                score = s
                best = item
        if best: resp = best["response"]
        else: resp = f"No answer found for '{query}'"
        self.history.append({"query": query, "response": resp, "timestamp": datetime.now().isoformat()})
        return resp

if "engine" not in st.session_state:
    st.session_state.engine = ARSLMEngine()

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/667eea/ffffff?text=MicroLLM", use_container_width=True)
    page = st.radio("Navigation", ["🏠 Dashboard", "💬 Chat"], label_visibility="collapsed")

# ===============================
# DASHBOARD
# ===============================
if page == "🏠 Dashboard":
    st.markdown('<p class="main-header">MicroLLM Studio</p>', unsafe_allow_html=True)
    st.markdown("Ultra-Light IA Assistant Local pour documents et code.")
    
    col1, col2 = st.columns(2)
    col1.markdown(f'<div class="metric-card">Messages<br><h2>{len(st.session_state.messages)}</h2></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="metric-card">Knowledge Base<br><h2>{len(st.session_state.engine.knowledge_base)}</h2></div>', unsafe_allow_html=True)

# ===============================
# CHAT
# ===============================
elif page == "💬 Chat":
    st.markdown('<p class="main-header">MicroLLM Chat</p>', unsafe_allow_html=True)

    # Affiche l'historique
    for msg in st.session_state.messages:
        cls = "user-msg" if msg["role"]=="user" else "assistant-msg"
        st.markdown(f'<div class="{cls}">{msg["content"]}</div>', unsafe_allow_html=True)

    # Input utilisateur
    user_input = st.chat_input("Pose ta question...")
    if user_input:
        st.session_state.messages.append({"role":"user","content":user_input})
        response = st.session_state.engine.generate_response(user_input)
        st.session_state.messages.append({"role":"assistant","content":response})
        st.experimental_rerun()

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.markdown("<div style='text-align:center;color:#777'>MicroLLM Studio · Local No-Code AI</div>", unsafe_allow_html=True)