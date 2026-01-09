"""
MicroLLM Studio - Enterprise AI Assistant
Powered by OpenAI (pluggable with ARSLM later)

© 2025 Benjamin Amaad Kama
"""

import streamlit as st
from pathlib import Path
from datetime import datetime

from openai import OpenAI
from pypdf import PdfReader
from docx import Document

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="MicroLLM Studio",
    page_icon="🤖",
    layout="wide"
)

# ==================================================
# OPENAI CLIENT
# ==================================================
client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))

# ==================================================
# DOMAINS
# ==================================================
DOMAINS = {
    "💻 Développement & Code": {
        "system_prompt": "Tu es un expert senior en développement logiciel et architecture."
    },
    "⚖️ Juridique": {
        "system_prompt": "Tu es un assistant juridique (informatif, pas de conseil légal)."
    },
    "💼 RH & Recrutement": {
        "system_prompt": "Tu es un expert RH et recrutement."
    },
    "🏥 Médical": {
        "system_prompt": "Tu es un assistant médical réservé aux professionnels de santé."
    },
    "📊 Business & Analyse": {
        "system_prompt": "Tu es un expert en business intelligence et analyse stratégique."
    }
}

# ==================================================
# SESSION STATE
# ==================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "domain" not in st.session_state:
    st.session_state.domain = list(DOMAINS.keys())[0]

if "knowledge_base" not in st.session_state:
    st.session_state.knowledge_base = []

# ==================================================
# HEADER
# ==================================================
st.markdown(
    """
    <div style="background:linear-gradient(135deg,#1e3c72,#667eea);
                padding:2rem;border-radius:15px;color:white;">
        <h1>🤖 MicroLLM Studio</h1>
        <p>Secure • On-Premise • Document-Aware AI</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ==================================================
# SIDEBAR
# ==================================================
with st.sidebar:
    st.markdown("## 🎯 Domaine")
    st.session_state.domain = st.selectbox(
        "Spécialisation",
        list(DOMAINS.keys())
    )

    st.markdown("---")
    st.markdown("## 📚 Ingestion Documents")

    uploaded_files = st.file_uploader(
        "PDF / Word / Code",
        type=["pdf", "docx", "txt", "py", "js", "ts", "java", "cpp"],
        accept_multiple_files=True
    )

    if uploaded_files:
        for file in uploaded_files:
            suffix = Path(file.name).suffix.lower()
            text = ""

            if suffix == ".pdf":
                reader = PdfReader(file)
                text = "\n".join(p.extract_text() or "" for p in reader.pages)

            elif suffix == ".docx":
                doc = Document(file)
                text = "\n".join(p.text for p in doc.paragraphs)

            else:
                text = file.read().decode("utf-8", errors="ignore")

            if text.strip():
                st.session_state.knowledge_base.append({
                    "name": file.name,
                    "content": text
                })
                st.success(f"✔ {file.name} ingéré")

    st.markdown("---")
    st.caption("🔐 Données traitées localement (session)")

# ==================================================
# CONTEXT BUILDER (RAG SIMPLE)
# ==================================================
def build_context():
    docs = st.session_state.knowledge_base[-5:]
    if not docs:
        return ""

    return "\n\n".join(
        f"### Document: {d['name']}\n{d['content'][:3000]}"
        for d in docs
    )

# ==================================================
# OPENAI RESPONSE
# ==================================================
def generate_response(user_query: str) -> str:
    domain_prompt = DOMAINS[st.session_state.domain]["system_prompt"]
    context = build_context()

    messages = [
        {"role": "system", "content": domain_prompt},
        {
            "role": "system",
            "content": (
                "Contexte interne issu de documents privés. "
                "Utilise-le uniquement s'il est pertinent.\n\n"
                f"{context}"
            )
        },
        {"role": "user", "content": user_query}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3,
        max_tokens=800
    )

    return response.choices[0].message.content

# ==================================================
# CHAT UI
# ==================================================
st.markdown("## 💬 Assistant IA")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Pose ta question…")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("assistant"):
        with st.spinner("Analyse en cours…"):
            answer = generate_response(user_input)
            st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

# ==================================================
# FOOTER
# ==================================================
st.markdown(
    """
    <hr>
    <small>
    © 2025 MicroLLM Studio — OpenAI backend (ARSLM-ready)
    </small>
    """,
    unsafe_allow_html=True
)
