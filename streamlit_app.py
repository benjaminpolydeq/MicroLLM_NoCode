"""
MicroLLM Studio - ARSLM Document Chat
Lightweight, No-Code, On-Prem AI Assistant
Handles PDF/TXT document uploads with smart Q&A
"""

import streamlit as st
import PyPDF2
import pandas as pd
from datetime import datetime

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="MicroLLM Studio",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# ARSLM INFO
# ===============================
ARSLM_INFO = {
    "name": "ARSLM",
    "version": "1.0.0",
    "description": (
        "ARSLM – Lightweight, Efficient & Secure AI\n\n"
        "Posez des questions sur vos documents PDF/TXT et obtenez des réponses précises."
    )
}

# ===============================
# CUSTOM CSS
# ===============================
st.markdown("""
<style>
* {font-family: 'Inter', sans-serif;}
.main-header {font-size:3rem;font-weight:bold;background:linear-gradient(90deg,#667eea 0%,#764ba2 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:1rem;}
.metric-card {background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);padding:20px;border-radius:15px;color:white;text-align:center;box-shadow:0px 5px 15px rgba(0,0,0,0.2);transition:transform 0.2s;cursor:pointer;margin:10px 0;}
.metric-card:hover {transform:scale(1.05);}
.metric-value {font-size:2.5rem;font-weight:bold;margin:10px 0;}
.metric-label {font-size:0.9rem;opacity:0.9;text-transform:uppercase;letter-spacing:1px;}
.user-msg {background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;padding:15px;border-radius:15px;margin:10px 0;margin-left:20%;box-shadow:0 2px 5px rgba(0,0,0,0.1);}
.assistant-msg {background:#f7f7f8;color:#1a1a1a;padding:15px;border-radius:15px;margin:10px 0;margin-right:20%;border-left:4px solid #667eea;box-shadow:0 2px 5px rgba(0,0,0,0.1);}
.info-box {background:linear-gradient(135deg,rgba(102,126,234,0.1)0%,rgba(118,75,162,0.1)100%);border-left:4px solid #667eea;padding:15px;border-radius:8px;margin:15px 0;}
.stButton button {background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;border:none;border-radius:8px;padding:10px 20px;font-weight:600;transition:all 0.3s ease;}
.stButton button:hover {transform:translateY(-2px);box-shadow:0 4px 12px rgba(102,126,234,0.4);}
</style>
""", unsafe_allow_html=True)

# ===============================
# SESSION STATE
# ===============================
if "uploaded_text" not in st.session_state:
    st.session_state.uploaded_text = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "engine" not in st.session_state:
    st.session_state.engine = None
if "models" not in st.session_state:
    st.session_state.models = []
if "training_history" not in st.session_state:
    st.session_state.training_history = []

# ===============================
# ARSLM ENGINE
# ===============================
class ARSLMEngine:
    def __init__(self, doc_text=""):
        self.conversation_history = []
        self.doc_text = doc_text
    
    def generate_response(self, query):
        q = query.lower()
        response = ""

        # Analyse du document
        if self.doc_text:
            if "titre" in q or "title" in q:
                response = f"📄 Le titre du document semble être : {self.doc_text.splitlines()[0]}"
            elif "résumé" in q or "summary" in q:
                lines = self.doc_text.splitlines()
                response = "📑 Résumé du document :\n" + "\n".join(lines[:5])
            elif "informations clé" in q or "key information" in q:
                key_lines = [line for line in self.doc_text.splitlines() if any(k in line.lower() for k in ["objectif","résultat","important","conclusion"])]
                response = "🔑 Informations clés :\n" + ("\n".join(key_lines) if key_lines else "Aucune information clé détectée.")
            else:
                response = "🤔 Essayez : 'titre', 'résumé', 'informations clé'."
        else:
            response = "📂 Aucun document chargé. Veuillez uploader un fichier PDF ou TXT."

        # Historique
        self.conversation_history.append({"query":query,"response":response,"timestamp":datetime.now().isoformat()})
        return response

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/667eea/ffffff?text=MicroLLM", use_container_width=True)
    st.markdown("---")
    page = st.radio("Navigation", ["🏠 Dashboard", "💬 Chat", "📊 Analytics", "⚙️ Settings"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("### 📊 System Status")
    st.success("🟢 Active")
    st.metric("Models", len(st.session_state.models))
    st.metric("Conversations", len(st.session_state.messages))
    st.markdown("---")
    st.info(f"**{ARSLM_INFO['name']}** v{ARSLM_INFO['version']}")

# ===============================
# DASHBOARD
# ===============================
if page == "🏠 Dashboard":
    st.markdown('<p class="main-header">MicroLLM Studio</p>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-box">{ARSLM_INFO["description"]}</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Active Models", len(st.session_state.models))
    col2.metric("Conversations", len(st.session_state.messages))
    col3.metric("Status", "✓")
    col4.metric("Security", "🔒")

# ===============================
# UPLOAD + CHAT
# ===============================
if page == "💬 Chat":
    st.markdown('<p class="main-header">Document Chat</p>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload PDF ou TXT", type=["pdf","txt"])
    
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page_pdf in pdf_reader.pages:
                text += page_pdf.extract_text() + "\n"
        else:
            text = uploaded_file.getvalue().decode("utf-8")
        
        st.session_state.uploaded_text = text
        st.success("📂 Document chargé !")
        st.session_state.engine = ARSLMEngine(doc_text=text)
    
    if st.session_state.engine:
        user_input = st.text_input("Posez une question sur le document :")
        if user_input:
            st.session_state.messages.append({"role":"user","content":user_input})
            response = st.session_state.engine.generate_response(user_input)
            st.session_state.messages.append({"role":"assistant","content":response})
        
        for msg in st.session_state.messages:
            cls = "user-msg" if msg["role"]=="user" else "assistant-msg"
            st.markdown(f'<div class="{cls}">{msg["content"]}</div>', unsafe_allow_html=True)

# ===============================
# ANALYTICS
# ===============================
elif page == "📊 Analytics":
    st.markdown('<p class="main-header">Analytics</p>', unsafe_allow_html=True)
    if st.session_state.engine and st.session_state.engine.conversation_history:
        df = pd.DataFrame(st.session_state.engine.conversation_history)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aucune donnée disponible. Posez une question sur un document d'abord.")

# ===============================
# SETTINGS
# ===============================
elif page == "⚙️ Settings":
    st.markdown('<p class="main-header">Settings</p>', unsafe_allow_html=True)
    st.checkbox("Enable encryption", value=True, disabled=True)
    st.checkbox("Audit logging", value=True, disabled=True)
    st.checkbox("Data anonymization", value=False)
    if st.button("Clear Conversation History"):
        st.session_state.messages = []
        if st.session_state.engine:
            st.session_state.engine.conversation_history = []
        st.success("✅ Historique effacé !")

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#666;padding:1rem">
    <strong>MicroLLM Studio</strong> · Built on ARSLM · Proprietary AI<br>
    © 2025 Benjamin Amaad Kama
</div>
""", unsafe_allow_html=True)