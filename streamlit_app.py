"""
MicroLLM Studio - Lightweight Multilingual Version
Supports PDF, TXT, DOCX uploads and chat
No PyTorch required - Pure Python implementation
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import json
import os
from langdetect import detect
from translate import Translator
from PyPDF2 import PdfReader
from docx import Document

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
# STYLES
# ===============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.main-header {
    font-size: 3rem;
    font-weight: bold;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1rem;
}

.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.2);
    transition: transform 0.2s;
    cursor: pointer;
    margin: 10px 0;
}

.metric-card:hover { transform: scale(1.05); }

.metric-value { font-size: 2.5rem; font-weight: bold; margin: 10px 0; }
.metric-label { font-size: 0.9rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px; }

.user-msg {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 15px;
    border-radius: 15px;
    margin: 10px 0;
    margin-left: 20%;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.assistant-msg {
    background: #f7f7f8;
    color: #1a1a1a;
    padding: 15px;
    border-radius: 15px;
    margin: 10px 0;
    margin-right: 20%;
    border-left: 4px solid #667eea;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.info-box {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    border-left: 4px solid #667eea;
    padding: 15px;
    border-radius: 8px;
    margin: 15px 0;
}

.stButton button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}
</style>
""", unsafe_allow_html=True)

# ===============================
# ARSLM / MicroLLM Engine
# ===============================
class MicroLLM:
    """Lightweight multilingual engine with file upload support"""
    def __init__(self):
        self.knowledge_base = []
        self.conversation_history = []
        self.documents = {}  # filename: text

    def add_document(self, filename, text):
        self.documents[filename] = text

    def generate_response(self, query, lang='fr'):
        query_lower = query.lower()
        # If query asks about uploaded documents
        if "document" in query_lower or "résumé" in query_lower or "summary" in query_lower:
            if not self.documents:
                response = "⚠️ Aucun document n'a été téléchargé."
            else:
                response_list = []
                for fname, content in self.documents.items():
                    summary = self.summarize_text(content)
                    response_list.append(f"📄 **{fname}**\n{summary}")
                response = "\n\n".join(response_list)
        else:
            response = f"🤔 Je n'ai pas de réponse spécifique pour **'{query}'**."
        
        # Translate if needed
        if lang != 'fr':
            translator = Translator(to_lang=lang)
            try:
                response = translator.translate(response)
            except:
                response = response + f"\n\n⚠️ Translation to {lang} failed."
        
        # Add to history
        self.conversation_history.append({
            "query": query,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
        return response

    def summarize_text(self, text, max_sentences=3):
        """Very simple extractive summary"""
        sentences = text.split(".")
        summary = ". ".join(sentences[:max_sentences])
        return summary.strip() + "."

# ===============================
# SESSION STATE
# ===============================
if "engine" not in st.session_state:
    st.session_state.engine = MicroLLM()
if "messages" not in st.session_state:
    st.session_state.messages = []

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/667eea/ffffff?text=MicroLLM+Studio", use_container_width=True)
    st.markdown("---")
    page = st.radio("Navigation", ["🏠 Dashboard", "💬 Chat", "⚙️ Settings"], label_visibility="collapsed")
    st.markdown("---")
    st.info("MicroLLM Studio\nVersion 1.0.0\n© 2026 Benjamin Amaad Kama")

# ===============================
# DASHBOARD
# ===============================
if page == "🏠 Dashboard":
    st.markdown('<p class="main-header">MicroLLM Studio</p>', unsafe_allow_html=True)
    st.caption("Lightweight, Multilingual AI – On-Premise & No-Code")

    # Quick metrics
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Conversations</div><div class="metric-value">{len(st.session_state.messages)}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Documents Uploaded</div><div class="metric-value">{len(st.session_state.engine.documents)}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📄 Upload Documents")
    uploaded_files = st.file_uploader("Upload PDF, TXT, DOCX", type=["pdf","txt","docx"], accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        content = ""
        if uploaded_file.type == "application/pdf":
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                content += page.extract_text() + "\n"
        elif uploaded_file.type == "text/plain":
            content = str(uploaded_file.read(), "utf-8")
        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            doc = Document(uploaded_file)
            for para in doc.paragraphs:
                content += para.text + "\n"
        st.session_state.engine.add_document(uploaded_file.name, content)
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} document(s) uploaded.")

# ===============================
# CHAT
# ===============================
elif page == "💬 Chat":
    st.markdown('<p class="main-header">MicroLLM Chat</p>', unsafe_allow_html=True)
    st.caption("Ask questions about your uploaded documents")

    # Language selection
    lang = st.selectbox("Select Language / Sélectionner la langue", ["fr","en","es"], index=0)

    # Display conversation
    for msg in st.session_state.messages:
        cls = "user-msg" if msg["role"]=="user" else "assistant-msg"
        st.markdown(f'<div class="{cls}">{"👤" if msg["role"]=="user" else "🤖"} {msg["content"]}</div>', unsafe_allow_html=True)

    # Input
    user_input = st.chat_input("Type your question / Posez votre question...")
    if user_input:
        st.session_state.messages.append({"role":"user","content":user_input})
        with st.spinner("🤔 MicroLLM is thinking..."):
            response = st.session_state.engine.generate_response(user_input, lang=lang)
        st.session_state.messages.append({"role":"assistant","content":response})
        st.rerun()

# ===============================
# SETTINGS
# ===============================
elif page == "⚙️ Settings":
    st.markdown('<p class="main-header">Settings</p>', unsafe_allow_html=True)
    if st.button("Clear Conversation History"):
        st.session_state.messages = []
        st.session_state.engine.conversation_history = []
        st.success("✅ History cleared")