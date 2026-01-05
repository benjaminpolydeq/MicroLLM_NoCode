"""
MicroLLM Studio - Lightweight Version for Streamlit Cloud
Supports PDF, TXT, DOCX Upload
Multilingual FR / EN / ES (no external translation)
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import json
import time
from tqdm import tqdm
from langdetect import detect

# File processing
import PyPDF2
import docx

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
# CUSTOM CSS (inchangé)
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
}

.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin: 10px 0;
}

.user-msg {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 15px;
    border-radius: 15px;
    margin: 10px 0;
    margin-left: 20%;
}

.assistant-msg {
    background: #f7f7f8;
    color: #1a1a1a;
    padding: 15px;
    border-radius: 15px;
    margin: 10px 0;
    margin-right: 20%;
    border-left: 4px solid #667eea;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# ARSLM ENGINE (RULE-BASED)
# ===============================
class ARSLMEngine:
    def __init__(self):
        self.history = []

    def generate_response(self, query, lang="en"):
        q = query.lower()

        if any(k in q for k in ["title", "titre", "título"]):
            return {
                "fr": "Le titre du document correspond généralement à la première section.",
                "en": "The document title is usually found at the beginning.",
                "es": "El título del documento suele estar al inicio."
            }[lang]

        if any(k in q for k in ["summary", "résumé", "resumen"]):
            return {
                "fr": "Voici un résumé basé sur le contenu du document.",
                "en": "Here is a summary based on the document content.",
                "es": "Aquí hay un resumen basado en el contenido del documento."
            }[lang]

        if any(k in q for k in ["key", "clé", "clave"]):
            return {
                "fr": "Les informations clés sont extraites des premières sections.",
                "en": "Key information is extracted from the main sections.",
                "es": "La información clave se extrae de las secciones principales."
            }[lang]

        return {
            "fr": "Je n'ai pas trouvé de réponse précise dans le document.",
            "en": "I could not find a precise answer in the document.",
            "es": "No se encontró una respuesta precisa en el documento."
        }[lang]

# ===============================
# SESSION STATE
# ===============================
if "engine" not in st.session_state:
    st.session_state.engine = ARSLMEngine()
if "messages" not in st.session_state:
    st.session_state.messages = []

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/667eea/ffffff?text=MicroLLM+Studio")
    page = st.radio("Navigation", ["🏠 Dashboard", "💬 Chat"], label_visibility="collapsed")

# ===============================
# FILE EXTRACTION
# ===============================
def extract_text(file):
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        return " ".join(page.extract_text() or "" for page in reader.pages)

    if file.type == "text/plain":
        return file.read().decode("utf-8", errors="ignore")

    if file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        d = docx.Document(file)
        return " ".join(p.text for p in d.paragraphs)

    return ""

def summarize_text(text):
    sentences = text.split(". ")
    return ". ".join(sentences[:5]) + "..." if len(sentences) > 5 else text

# ===============================
# DASHBOARD
# ===============================
if page == "🏠 Dashboard":
    st.markdown('<p class="main-header">MicroLLM Studio</p>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("📄 Upload PDF, TXT ou DOCX", type=["pdf","txt","docx"])

    if uploaded_file:
        with st.spinner("📖 Extraction du texte..."):
            text_content = extract_text(uploaded_file)
            st.success("✅ Texte extrait")

        st.text_area("Contenu extrait", text_content, height=200)

        st.markdown("### ⏳ Analyse")
        progress = st.progress(0)
        for i in tqdm(range(100)):
            time.sleep(0.01)
            progress.progress(i + 1)

        st.markdown("### 📋 Résumé")
        st.write(summarize_text(text_content))

# ===============================
# CHAT
# ===============================
elif page == "💬 Chat":
    st.markdown('<p class="main-header">MicroLLM Chat</p>', unsafe_allow_html=True)

    for msg in st.session_state.messages:
        cls = "user-msg" if msg["role"] == "user" else "assistant-msg"
        st.markdown(
            f'<div class="{cls}">{"👤" if msg["role"]=="user" else "🤖"} {msg["content"]}</div>',
            unsafe_allow_html=True
        )

    user_input = st.chat_input("Posez votre question sur le document...")

    if user_input:
        try:
            lang = detect(user_input)
            if lang not in ["fr", "en", "es"]:
                lang = "en"
        except:
            lang = "en"

        response = st.session_state.engine.generate_response(user_input, lang)

        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()