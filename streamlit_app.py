"""
MicroLLM Studio - Lightweight Version for Streamlit Cloud
Supports PDF, TXT, DOCX Upload, Multilingual (FR/EN/ES)
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import json
import re
from tqdm import tqdm
import time

# File processing
import PyPDF2
import docx
import magic
from googletrans import Translator

translator = Translator()

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
# CUSTOM CSS
# ===============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');  
* { font-family: 'Inter', sans-serif; }  

.main-header {  
    font-size: 3rem; font-weight: bold; 
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);  
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
    margin-bottom: 1rem;  
}

.metric-card {  
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);  
    padding: 20px; border-radius: 15px; color: white; text-align: center; 
    box-shadow: 0px 5px 15px rgba(0,0,0,0.2); transition: transform 0.2s; cursor: pointer; margin: 10px 0;  
}  
.metric-card:hover { transform: scale(1.05); }  
.metric-value { font-size: 2.5rem; font-weight: bold; margin: 10px 0; }  
.metric-label { font-size: 0.9rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px; }  

.user-msg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; border-radius: 15px; margin: 10px 0; margin-left: 20%; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }  
.assistant-msg { background: #f7f7f8; color: #1a1a1a; padding: 15px; border-radius: 15px; margin: 10px 0; margin-right: 20%; border-left: 4px solid #667eea; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }  

.stButton button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; padding: 10px 20px; font-weight: 600; transition: all 0.3s ease; }  
.stButton button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4); }  

</style>
""", unsafe_allow_html=True)

# ===============================
# ARSLM Engine (Lightweight)
# ===============================
class ARSLMEngine:
    """Lightweight MicroLLM engine without PyTorch"""
    def __init__(self):
        self.knowledge_base = self._load_knowledge_base()
        self.conversation_history = []

    def _load_knowledge_base(self):
        return [
            {"keywords": ["what is", "qu'est-ce", "definition"], "response": "This is MicroLLM Studio - lightweight AI engine..."},
            {"keywords": ["features", "fonctionnalités"], "response": "Features: Multilingual chat, PDF/TXT/DOCX upload, summary generation, lightweight design."},
            {"keywords": ["install", "setup"], "response": "Install: pip install -r requirements.txt; run streamlit_app.py"},
        ]

    def generate_response(self, query):
        query_lower = query.lower()
        best_match = None
        best_score = 0
        for item in self.knowledge_base:
            score = sum(1 for kw in item["keywords"] if kw in query_lower)
            if score > best_score:
                best_score = score
                best_match = item
        if best_match and best_score > 0:
            response = best_match["response"]
        else:
            response = f"No specific answer for '{query}'"
        self.conversation_history.append({"query": query, "response": response, "timestamp": datetime.now().isoformat()})
        return response

# ===============================
# SESSION STATE
# ===============================
if "engine" not in st.session_state: st.session_state.engine = ARSLMEngine()
if "messages" not in st.session_state: st.session_state.messages = []

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/667eea/ffffff?text=MicroLLM+Studio", use_container_width=True)
    st.markdown("---")
    page = st.radio("Navigation", ["🏠 Dashboard", "💬 Chat"], label_visibility="collapsed")

# ===============================
# File Processing
# ===============================
def extract_text(file):
    file_type = magic.from_buffer(file.read(1024), mime=True)
    file.seek(0)
    if file_type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        text = " ".join([page.extract_text() for page in reader.pages])
    elif file_type in ["text/plain", "text/csv"]:
        text = file.read().decode("utf-8")
    elif file_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        doc = docx.Document(file)
        text = " ".join([p.text for p in doc.paragraphs])
    else:
        text = ""
    return text

def translate_text(text, target_lang="fr"):
    try:
        detected = translator.detect(text).lang
        if detected != target_lang:
            translated = translator.translate(text, dest=target_lang)
            return translated.text
        else:
            return text
    except:
        return text

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
            st.success("✅ Texte extrait !")
            st.text_area("Contenu", text_content, height=200)
        st.markdown("### ⏳ Analyse")
        progress_bar = st.progress(0)
        for i in tqdm(range(100)):
            time.sleep(0.01)
            progress_bar.progress(i+1)
        st.markdown("### 📋 Résumé")
        st.write(summarize_text(text_content))

# ===============================
# CHAT
# ===============================
elif page == "💬 Chat":
    st.markdown('<p class="main-header">MicroLLM Chat</p>', unsafe_allow_html=True)
    if not st.session_state.messages:
        st.markdown('<div class="assistant-msg">👋 Bienvenue sur MicroLLM Chat !</div>', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        cls = "user-msg" if msg["role"]=="user" else "assistant-msg"
        st.markdown(f'<div class="{cls}">{"👤" if msg["role"]=="user" else "🤖"} {msg["content"]}</div>', unsafe_allow_html=True)
    user_input = st.chat_input("Posez votre question...")
    if user_input:
        detected_lang = translator.detect(user_input).lang
        user_input_translated = translate_text(user_input, target_lang="en")
        response = st.session_state.engine.generate_response(user_input_translated)
        response_translated = translate_text(response, target_lang=detected_lang)
        st.session_state.messages.append({"role":"user","content":user_input})
        st.session_state.messages.append({"role":"assistant","content":response_translated})
        st.rerun()