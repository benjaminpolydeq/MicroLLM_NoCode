"""
MicroLLM Studio - Enterprise On-Premise AI Assistant
Version stable et sécurisée
© 2025 Benjamin Amaad Kama
"""

import streamlit as st
from datetime import datetime
import PyPDF2
import docx

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
# OPENAI SDK (NEW)
# ===============================
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# ===============================
# SYSTEM INFO
# ===============================
SYSTEM_INFO = {
    "platform": "MicroLLM Studio",
    "version": "1.6.1-Stable",
    "base_model": "ARSLM / OpenAI Compatible",
}

# ===============================
# DOMAINS
# ===============================
DOMAINS = {
    "💼 RH & Recrutement": "Tu es un expert RH et recrutement. Réponds de manière professionnelle et confidentielle.",
    "⚖️ Juridique & Compliance": "Tu es un assistant juridique. Réponses informatives uniquement, jamais de conseil légal.",
    "🏥 Médical & Santé": "Tu es un assistant médical. Ne remplace jamais un avis médical.",
    "🔬 Recherche & Sciences": "Tu es un assistant scientifique rigoureux et factuel.",
    "💻 Développement & Code": "Tu es un expert logiciel senior.",
    "📊 Analyse & Business Intelligence": "Tu es un expert data orienté décisions.",
}

# ===============================
# SESSION STATE
# ===============================
st.session_state.setdefault("messages", [])
st.session_state.setdefault("current_domain", "💼 RH & Recrutement")
st.session_state.setdefault("extracted_text", "")

# ===============================
# SIDEBAR - API
# ===============================
st.sidebar.title("🔐 Configuration API")

api_key = st.secrets.get("OPENAI_API_KEY") if hasattr(st, "secrets") else None
if not api_key:
    api_key = st.sidebar.text_input("Clé API OpenAI", type="password")

if api_key:
    st.sidebar.success("✅ API configurée")
else:
    st.sidebar.warning("⚠️ Clé API manquante")

MODEL_LIST = [
    "gpt-4.1-mini",
    "gpt-4.1",
    "gpt-4o"
]

model_name = st.sidebar.selectbox("Modèle IA", MODEL_LIST)

selected_domain = st.sidebar.selectbox(
    "🎯 Domaine",
    list(DOMAINS.keys()),
    index=list(DOMAINS.keys()).index(st.session_state.current_domain)
)
st.session_state.current_domain = selected_domain

if st.sidebar.button("🗑️ Effacer l'historique"):
    st.session_state.messages = []
    st.session_state.extracted_text = ""
    st.rerun()

# ===============================
# HEADER
# ===============================
st.markdown(
    f"""
    <div style="background:linear-gradient(135deg,#1e3c72,#667eea);
    padding:2rem;border-radius:12px;color:white;">
    <h1>🤖 MicroLLM Studio</h1>
    <small>Version {SYSTEM_INFO['version']}</small>
    </div>
    """,
    unsafe_allow_html=True
)

# ===============================
# AI ENGINE (NEW API)
# ===============================
def call_ai_api(prompt: str, domain: str) -> str:
    if not api_key:
        return "❌ Clé API manquante."
    if not OPENAI_AVAILABLE:
        return "❌ SDK OpenAI non installé."

    try:
        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model=model_name,
            input=[
                {
                    "role": "system",
                    "content": DOMAINS.get(domain)
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_output_tokens=2000
        )

        return response.output_text

    except Exception as e:
        return f"❌ Erreur API: {str(e)}"

# ===============================
# FILE EXTRACTION
# ===============================
def extract_text(uploaded_file):
    text = ""
    if uploaded_file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(uploaded_file)
        for p in reader.pages:
            text += p.extract_text() or ""
    elif uploaded_file.name.endswith(".docx"):
        doc = docx.Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    elif uploaded_file.name.endswith(".txt"):
        text = uploaded_file.read().decode("utf-8")
    return text.strip()

# ===============================
# TABS
# ===============================
tab1, tab2 = st.tabs(["💬 Chat", "📄 Documents"])

# CHAT
with tab1:
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).markdown(msg["content"])

    user_input = st.chat_input("Posez votre question...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        answer = call_ai_api(user_input, st.session_state.current_domain)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()

# DOCUMENTS
with tab2:
    file = st.file_uploader("PDF / DOCX / TXT", type=["pdf", "docx", "txt"])
    if file:
        st.session_state.extracted_text = extract_text(file)
        st.text_area("Texte extrait", st.session_state.extracted_text, height=300)

        if st.button("🧠 Analyser"):
            prompt = f"Analyse ce document:\n{st.session_state.extracted_text[:4000]}"
            answer = call_ai_api(prompt, st.session_state.current_domain)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.success("Analyse envoyée au chat.")

# ===============================
# FOOTER
# ===============================
st.markdown(
    f"<center>© {datetime.now().year} MicroLLM Studio | flywithjesus@outlook.com</center>",
    unsafe_allow_html=True
)