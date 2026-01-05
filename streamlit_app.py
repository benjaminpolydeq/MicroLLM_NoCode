import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import json
import os
import re
from langdetect import detect
from googletrans import Translator  # pip install googletrans==4.0.0-rc1
from PyPDF2 import PdfReader  # pip install PyPDF2
from docx import Document  # pip install python-docx

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
# INFO & CSS
# ===============================
APP_INFO = {
    "name": "MicroLLM Studio",
    "version": "1.0.0-MVP",
    "description": (
        "MicroLLM Studio – Lightweight, Efficient & Secure AI\n"
        "Supports multiple languages: 🇫🇷 🇬🇧 🇪🇸\n"
        "Upload documents and ask questions directly."
    )
}

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
    transition: all 0.3s ease;
}
.main-header:hover { transform: scale(1.05); }

.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.2);
    transition: transform 0.3s ease;
    cursor: pointer;
    margin: 10px 0;
}
.metric-card:hover { transform: scale(1.05); }

.user-msg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; border-radius: 15px; margin: 10px 0; margin-left: 20%; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
.assistant-msg { background: #f7f7f8; color: #1a1a1a; padding: 15px; border-radius: 15px; margin: 10px 0; margin-right: 20%; border-left: 4px solid #667eea; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }

.info-box { background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); border-left: 4px solid #667eea; padding: 15px; border-radius: 8px; margin: 15px 0; }
</style>
""", unsafe_allow_html=True)

# ===============================
# ENGINE
# ===============================
class MicroLLMEngine:
    def __init__(self):
        self.conversation_history = []
        self.documents = {}  # key=file_name, value=text
        self.translator = Translator()

    def add_document(self, file_name, text):
        self.documents[file_name] = text

    def extract_text_from_file(self, uploaded_file):
        name = uploaded_file.name
        if name.endswith(".pdf"):
            pdf = PdfReader(uploaded_file)
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
            return text
        elif name.endswith(".txt"):
            return uploaded_file.read().decode("utf-8")
        elif name.endswith(".docx"):
            doc = Document(uploaded_file)
            text = "\n".join([p.text for p in doc.paragraphs])
            return text
        else:
            return ""

    def generate_response(self, query, lang="fr"):
        # Detect language
        try:
            detected_lang = detect(query)
        except:
            detected_lang = "fr"

        # If document-related question
        response = ""
        for fname, text in self.documents.items():
            if re.search(r"(title|titre|resumen|summary|résumé)", query, re.I):
                response += f"📄 **File:** {fname}\n"
                lines = text.split("\n")
                response += f"**Title / First line:** {lines[0]}\n\n"
            if re.search(r"(summary|résumé|resumen)", query, re.I):
                summary = "\n".join(text.split("\n")[:5])
                response += f"**Summary:**\n{summary}\n\n"
            if re.search(r"(key info|informations clés|información clave)", query, re.I):
                keywords = re.findall(r"\b[A-Z][a-z]+\b", text)
                top_keys = ", ".join(keywords[:10])
                response += f"**Key Info:** {top_keys}\n\n"

        if not response:
            response = f"🤔 Je n'ai pas de réponse spécifique pour **\"{query}\"**"

        # Translate if needed
        if lang != "fr":
            try:
                response = self.translator.translate(response, dest=lang).text
            except:
                pass

        self.conversation_history.append({
            "query": query,
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "lang": lang
        })
        return response

# ===============================
# SESSION STATE
# ===============================
if "engine" not in st.session_state:
    st.session_state.engine = MicroLLMEngine()
if "messages" not in st.session_state:
    st.session_state.messages = []

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/667eea/ffffff?text=MicroLLM+Studio", use_container_width=True)
    st.markdown("---")
    page = st.radio("Navigation", ["🏠 Dashboard", "💬 Chat", "📄 Documents", "⚙️ Settings"], label_visibility="collapsed")
    st.markdown("---")
    st.metric("Conversations", len(st.session_state.messages))
    st.info(f"**{APP_INFO['name']}** v{APP_INFO['version']}")

# ===============================
# DASHBOARD
# ===============================
if page == "🏠 Dashboard":
    st.markdown('<p class="main-header">MicroLLM Studio</p>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-box">{APP_INFO["description"]}</div>', unsafe_allow_html=True)

# ===============================
# DOCUMENTS
# ===============================
elif page == "📄 Documents":
    st.markdown('<p class="main-header">Upload & Analyze Documents</p>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Upload PDF, TXT, DOCX", accept_multiple_files=True)
    for f in uploaded_files:
        text = st.session_state.engine.extract_text_from_file(f)
        st.session_state.engine.add_document(f.name, text)
        st.success(f"✅ {f.name} uploaded and processed")

# ===============================
# CHAT
# ===============================
elif page == "💬 Chat":
    st.markdown('<p class="main-header">Chat with MicroLLM</p>', unsafe_allow_html=True)
    lang_choice = st.selectbox("Choose Language / Choisir la langue / Selecciona idioma", ["fr", "en", "es"])

    # Display messages
    for msg in st.session_state.messages:
        cls = "user-msg" if msg["role"] == "user" else "assistant-msg"
        st.markdown(f'<div class="{cls}">{"👤" if msg["role"]=="user" else "🤖"} {msg["content"]}</div>', unsafe_allow_html=True)

    user_input = st.chat_input("Ask a question / Posez une question / Haz una pregunta")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("🤔 MicroLLM is thinking..."):
            response = st.session_state.engine.generate_response(user_input, lang_choice)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# ===============================
# SETTINGS
# ===============================
elif page == "⚙️ Settings":
    st.markdown('<p class="main-header">Settings</p>', unsafe_allow_html=True)
    st.checkbox("Enable animations", value=True)
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.session_state.engine.conversation_history = []
        st.success("✅ Chat history cleared")