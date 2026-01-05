"""
ARSLM Chat Studio - Lightweight Version + Smart Highlight + Multilingual
Copyright © 2025 Benjamin Amaad Kama
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import json
import re
import PyPDF2
from langdetect import detect
from difflib import SequenceMatcher

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="ARSLM Studio",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# ARSLM INFO
# ===============================
ARSLM_INFO = {
    "name": "ARSLM",
    "version": "1.0.2-MVP",
    "description": (
        "ARSLM – Lightweight, Efficient & Secure AI\n\n"
        "Compact language model built for real-world applications, "
        "combining speed, efficiency, and adaptability. Runs on low-resource "
        "environments, ensures data privacy, intelligent text generation, "
        "document QA and smart highlighting in English, French, and Spanish."
    )
}

# ===============================
# CSS + Animations
# ===============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; transition: all 0.2s ease; }

.main-header { font-size:3rem; font-weight:bold; background:linear-gradient(90deg,#667eea,#764ba2); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:1rem; animation:fadeIn 1s ease-out; }
.metric-card { background:linear-gradient(135deg,#667eea 0%,#764ba2 100%); padding:20px; border-radius:15px; color:white; text-align:center; box-shadow:0px 5px 15px rgba(0,0,0,0.2); cursor:pointer; margin:10px 0; transition: all 0.3s ease; }
.metric-card:hover { transform: scale(1.08) rotate(0.5deg); box-shadow: 0 10px 20px rgba(0,0,0,0.3); }
.metric-value { font-size:2.5rem; font-weight:bold; margin:10px 0; }
.metric-label { font-size:0.9rem; opacity:0.9; text-transform:uppercase; letter-spacing:1px; }

.user-msg { background: linear-gradient(135deg,#667eea 0%,#764ba2 100%); color:white; padding:15px; border-radius:15px; margin:10px 0; margin-left:20%; box-shadow:0 2px 5px rgba(0,0,0,0.1); animation:slideInLeft 0.3s ease-out; }
.assistant-msg { background:#f7f7f8; color:#1a1a1a; padding:15px; border-radius:15px; margin:10px 0; margin-right:20%; border-left:4px solid #667eea; box-shadow:0 2px 5px rgba(0,0,0,0.1); animation:slideInRight 0.3s ease-out; }

.info-box { background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%); border-left:4px solid #667eea; padding:15px; border-radius:8px; margin:15px 0; animation:fadeIn 0.6s ease-out; }
.highlight { background-color: #FFF176; padding: 2px 4px; border-radius:3px; }

.stButton button { background: linear-gradient(135deg,#667eea 0%,#764ba2 100%); color:white; border:none; border-radius:8px; padding:10px 20px; font-weight:600; transition: all 0.3s ease; }
.stButton button:hover { transform: translateY(-2px) scale(1.05); box-shadow:0 6px 15px rgba(102,126,234,0.4); }

@keyframes slideInLeft { from {opacity:0; transform:translateX(-50px);} to {opacity:1; transform:translateX(0);} }
@keyframes slideInRight { from {opacity:0; transform:translateX(50px);} to {opacity:1; transform:translateX(0);} }
@keyframes fadeIn { from {opacity:0;} to {opacity:1;} }
</style>
""", unsafe_allow_html=True)

# ===============================
# ARSLM ENGINE + SMART DOCUMENT QA
# ===============================
class ARSLMEngine:
    def __init__(self):
        self.knowledge_base = self._load_knowledge_base()
        self.conversation_history = []
        self.document_text = ""
        self.document_sections = []

    def _load_knowledge_base(self):
        return [
            {"keywords":["arslm"], "response":"ARSLM est un modèle léger AI propriétaire pour entreprises."}
        ]

    # -----------------------------
    # DOCUMENT HANDLING
    # -----------------------------
    def load_document(self, file):
        if file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            self.document_text = text
        else:
            self.document_text = file.getvalue().decode("utf-8")
        # split into sentences for intelligent highlighting
        self.document_sections = [s.strip() for s in re.split(r'(?<=[.!?])\s+', self.document_text) if s.strip()]

    # -----------------------------
    # SMART HIGHLIGHT
    # -----------------------------
    def highlight_sentences(self, query: str, top_n: int = 5):
        """Highlight top N most relevant sentences for the query"""
        if not self.document_sections:
            return "Aucun document chargé."

        def similarity(a, b):
            return SequenceMatcher(None, a.lower(), b.lower()).ratio()

        scored = [(s, similarity(s, query)) for s in self.document_sections]
        scored.sort(key=lambda x: x[1], reverse=True)
        top_sentences = [s for s, score in scored[:top_n] if score > 0.1]

        highlighted_text = self.document_text
        for s in top_sentences:
            highlighted_text = highlighted_text.replace(s, f'<span class="highlight">{s}</span>')

        return highlighted_text.replace("\n", "<br>")

    # -----------------------------
    # DOCUMENT QA
    # -----------------------------
    def query_document(self, query: str):
        if not self.document_sections:
            return self.generate_response(query)

        lang = detect(query)  # detect language
        response = ""
        query_lower = query.lower()

        if any(k in query_lower for k in ["titre","title","título"]):
            title = self.document_sections[0] if self.document_sections else "Document sans titre"
            response = f"📄 Titre du document : {title}"
        elif any(k in query_lower for k in ["résumé","summary","resumen"]):
            summary = " ".join(self.document_sections[:5])
            response = f"📝 Résumé :\n{summary}"
        elif any(k in query_lower for k in ["informations","key info","información clave"]):
            key_info = " ".join(self.document_sections[:10])
            response = f"🔑 Informations clés :\n{key_info}"
        else:
            response = f"📄 Document chargé. Question reçue : {query}. Je peux donner titre, résumé et infos clés."

        self.conversation_history.append({"query": query, "response": response, "timestamp": datetime.now().isoformat()})
        return response

    # -----------------------------
    # GENERAL RESPONSE
    # -----------------------------
    def generate_response(self, query: str):
        best_match = None
        best_score = 0
        for item in self.knowledge_base:
            score = sum(1 for kw in item["keywords"] if kw in query.lower())
            if score > best_score:
                best_score = score
                best_match = item
        response = best_match["response"] if best_match else f"🤔 Je n'ai pas de réponse spécifique pour \"{query}\"."
        self.conversation_history.append({"query": query, "response": response, "timestamp": datetime.now().isoformat()})
        return response

# ===============================
# SESSION STATE
# ===============================
if "engine" not in st.session_state:
    st.session_state.engine = ARSLMEngine()
if "messages" not in st.session_state:
    st.session_state.messages = []

# ===============================
# CHAT PAGE
# ===============================
if st.sidebar.radio("Navigation", ["🏠 Dashboard", "💬 Chat", "📊 Analytics", "⚙️ Settings"]) == "💬 Chat":
    st.markdown('<p class="main-header">ARSLM Chat</p>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("📄 Charger un document (PDF/TXT)", type=["pdf","txt"])
    if uploaded_file:
        st.session_state.engine.load_document(uploaded_file)
        st.success("✅ Document chargé avec succès !")

    for msg in st.session_state.messages:
        cls = "user-msg" if msg["role"]=="user" else "assistant-msg"
        st.markdown(
            f'<div class="{cls}">{"👤" if msg["role"]=="user" else "🤖"} {msg["content"]}</div>',
            unsafe_allow_html=True
        )

    user_input = st.chat_input("Posez votre question...")
    if user_input:
        st.session_state.messages.append({"role":"user","content":user_input})
        with st.spinner("🤔 ARSLM réfléchit..."):
            response = st.session_state.engine.query_document(user_input)
        st.session_state.messages.append({"role":"assistant","content":response})
        # Show highlighted document (smart highlighting)
        if st.session_state.engine.document_text:
            st.markdown(
                "<div class='info-box'>" + st.session_state.engine.highlight_sentences(user_input) + "</div>",
                unsafe_allow_html=True
            )
        st.rerun()