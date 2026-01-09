"""
MicroLLM Studio - Enterprise On-Premise AI Assistant
API-enabled version (OpenAI-compatible)
Clé API sécurisée via st.secrets
"""

import os
import streamlit as st
from datetime import datetime
import PyPDF2
import docx

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="MicroLLM Studio - Enterprise AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# OPTIONAL: OpenAI SDK
# ===============================
try:
    from openai import OpenAI
except Exception:
    OpenAI = None

# ===============================
# SYSTEM INFO
# ===============================
SYSTEM_INFO = {
    "platform": "MicroLLM Studio",
    "version": "1.5.0-Enterprise-API",
    "base_model": "ARSLM / External LLM",
}

# ===============================
# DOMAINS
# ===============================
DOMAINS = {
    "💼 RH & Recrutement": "Tu es un expert RH et recrutement. Réponds de manière professionnelle et confidentielle.",
    "⚖️ Juridique & Compliance": "Tu es un assistant juridique. Réponses informatives uniquement, jamais de conseil légal.",
    "🏥 Médical & Santé": "Tu es un assistant médical pour professionnels de santé. Ne remplace jamais un avis médical.",
    "🔬 Recherche & Sciences": "Tu es un assistant de recherche scientifique rigoureux et factuel.",
    "💻 Développement & Code": "Tu es un expert en développement logiciel et architecture.",
    "📊 Analyse & Business Intelligence": "Tu es un expert data et business intelligence, orienté décisions.",
}

# ===============================
# SIDEBAR - API CONFIG
# ===============================
st.sidebar.title("🔐 Configuration API")

# 🔒 Récupération sécurisée de la clé via st.secrets
api_key = st.secrets.get("OPENAI_API_KEY", None)

if not api_key:
    st.sidebar.error("❌ Clé API OpenAI manquante ! Ajoutez-la dans st.secrets.toml")

model_name = st.sidebar.text_input(
    "Modèle",
    value="gpt-4o-mini"
)

st.sidebar.markdown("---")

selected_domain = st.sidebar.selectbox(
    "Domaine",
    list(DOMAINS.keys())
)

# ===============================
# HEADER
# ===============================
st.markdown(
    f"""
    <div style="background:linear-gradient(135deg,#1e3c72,#667eea);
                padding:2rem;border-radius:12px;color:white;">
        <h1>🤖 MicroLLM Studio</h1>
        <p>Enterprise AI Assistant – API Secure Mode</p>
        <small>Version {SYSTEM_INFO['version']}</small>
    </div>
    """,
    unsafe_allow_html=True
)

# ===============================
# SESSION STATE
# ===============================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ===============================
# AI ENGINE (API MODE)
# ===============================
def call_ai_api(user_query: str, domain: str) -> str:
    if not api_key:
        return "❌ Clé API manquante ou invalide. Veuillez ajouter votre clé dans st.secrets.toml"

    if OpenAI is None:
        return "❌ SDK OpenAI non installé. Ajoutez `openai` à requirements.txt."

    client = OpenAI(api_key=api_key)
    system_prompt = DOMAINS.get(domain, "Tu es un assistant professionnel.")

    messages = [{"role": "system", "content": system_prompt}]
    messages += st.session_state.messages[-6:]  # Historique limité
    messages.append({"role": "user", "content": user_query})

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Erreur API : {e}"

# ===============================
# PDF / DOCX / TXT UPLOAD
# ===============================
def extract_text_from_file(uploaded_file):
    if uploaded_file is None:
        return ""

    filename = uploaded_file.name.lower()
    text = ""

    if filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    elif filename.endswith(".docx"):
        doc = docx.Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    elif filename.endswith(".txt"):
        text = str(uploaded_file.read(), encoding='utf-8')
    else:
        st.warning("Format non supporté. Veuillez uploader un PDF, DOCX ou TXT.")
    return text.strip()

# ===============================
# CONTAINERS POUR CHAT ET DOC
# ===============================
doc_container = st.container()
chat_container = st.container()

# ===== Document Upload / Analyse =====
with doc_container:
    st.subheader("📄 Analyse de document")
    uploaded_file = st.file_uploader("Upload PDF, DOCX ou TXT", type=["pdf", "docx", "txt"])
    if uploaded_file:
        doc_text = extract_text_from_file(uploaded_file)
        if doc_text:
            st.text_area("Contenu extrait", value=doc_text, height=200)
            if st.button("Analyser le document", key="analyze_doc"):
                st.session_state.messages.append({"role": "user", "content": doc_text})
                answer = call_ai_api(doc_text, selected_domain)
                st.session_state.messages.append({"role": "assistant", "content": answer})

# ===== Chat UI =====
with chat_container:
    st.subheader(f"🧠 Domaine actif : {selected_domain}")
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f"<div style='background:#667eea;color:white;padding:1rem;border-radius:12px;margin:1rem 0 1rem 20%;'>{msg['content']}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div style='background:#f4f6f8;padding:1rem;border-radius:12px;margin:1rem 20% 1rem 0;border-left:4px solid #667eea;'>{msg['content']}</div>",
                unsafe_allow_html=True
            )

    user_input = st.text_area("Votre message", placeholder="Posez votre question…")
    if st.button("Envoyer", key="send_chat") and user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input})
        answer = call_ai_api(user_input, selected_domain)
        st.session_state.messages.append({"role": "assistant", "content": answer})

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.caption(f"© {datetime.now().year} MicroLLM Studio – Secure API Mode")