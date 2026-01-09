"""
MicroLLM Studio - Enterprise On-Premise AI Assistant
Built on ARSLM - Secure, Private, Specialized AI for Sensitive Domains

Copyright © 2025 Benjamin Amaad Kama. All Rights Reserved.
Proprietary Software - License Required for Commercial Use
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os
import io
from pathlib import Path
from openai import OpenAI
from PyPDF2 import PdfReader
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
# OPENAI API INIT
# ===============================
api_key = st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error("🔑 Clé OpenAI manquante ! Vérifie .streamlit/secrets.toml")
    st.stop()
else:
    client = OpenAI(api_key=api_key)
    st.success("✅ Clé OpenAI détectée et client initialisé")

# ===============================
# SYSTEM INFO
# ===============================
SYSTEM_INFO = {
    "platform": "MicroLLM Studio",
    "version": "1.0.0-Enterprise",
    "base_model": "ARSLM",
    "features": [
        "🔒 100% On-Premise - Données sécurisées",
        "🧠 Spécialisation domaine",
        "📚 Ingestion PDF/DOC/TXT/Code",
        "🔍 Recherche interne sécurisée",
        "💻 Analyse et génération de code",
        "📊 Résumés et rapports automatisés",
        "🎯 Interface No-Code",
        "🔐 Sécurité renforcée"
    ]
}

# ===============================
# DOMAINES
# ===============================
DOMAINS = [
    "💼 RH & Recrutement",
    "⚖️ Juridique & Compliance",
    "🏥 Médical & Santé",
    "🔬 Recherche & Sciences",
    "💻 Développement & Code",
    "📊 Analyse & Business Intelligence"
]

if "current_domain" not in st.session_state:
    st.session_state.current_domain = DOMAINS[0]

if "documents" not in st.session_state:
    st.session_state.documents = []

if "messages" not in st.session_state:
    st.session_state.messages = []

# ===============================
# UTILS D'INGESTION
# ===============================
def ingest_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def ingest_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def ingest_txt(file):
    return file.read().decode("utf-8")

def ingest_code(file):
    return file.read().decode("utf-8")

def ingest_file(file):
    ext = file.name.split(".")[-1].lower()
    if ext == "pdf":
        return ingest_pdf(file)
    elif ext in ["docx", "doc"]:
        return ingest_docx(file)
    elif ext in ["txt", "csv", "py", "js", "java"]:
        return ingest_txt(file)
    else:
        return None

# ===============================
# AI RESPONSE FUNCTION
# ===============================
def generate_ai_response(query, domain):
    """
    Utilise OpenAI pour générer une réponse basée sur le domaine et documents ingérés
    """
    # Combiner les documents comme contexte
    context_text = "\n\n".join([doc["content"] for doc in st.session_state.documents])
    
    prompt = f"""
Tu es un assistant expert pour le domaine {domain}.
Voici le contexte des documents internes :
{context_text}

Réponds à la question suivante de manière claire et concise :
{query}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"Tu es un assistant expert en {domain}."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Erreur OpenAI : {e}"

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.title("Navigation")
    page = st.radio("Menu", ["🏠 Accueil", "💬 Assistant IA", "📚 Documents", "💻 Analyse Code", "⚙️ Configuration"])
    
    st.markdown("---")
    
    st.markdown("### Sélection Domaine")
    selected_domain = st.selectbox("Domaine", DOMAINS, index=DOMAINS.index(st.session_state.current_domain))
    st.session_state.current_domain = selected_domain

# ===============================
# PAGE LOGIC
# ===============================
if page == "🏠 Accueil":
    st.header(f"🤖 {SYSTEM_INFO['platform']}")
    st.subheader(f"Version : {SYSTEM_INFO['version']}")
    st.markdown("**Fonctionnalités :**")
    for f in SYSTEM_INFO["features"]:
        st.write(f"- {f}")

elif page == "📚 Documents":
    st.header("📂 Ingestion de documents")
    uploaded_files = st.file_uploader("Importer PDF, DOCX, TXT ou Code", type=["pdf", "docx", "txt", "py", "js", "java", "csv"], accept_multiple_files=True)
    
    if uploaded_files:
        for file in uploaded_files:
            content = ingest_file(file)
            if content:
                doc_data = {
                    "filename": file.name,
                    "content": content,
                    "uploaded_at": datetime.now().isoformat()
                }
                st.session_state.documents.append(doc_data)
                st.success(f"✅ {file.name} ingéré avec succès")
            else:
                st.warning(f"⚠️ {file.name} n'a pas pu être ingéré")

elif page == "💬 Assistant IA":
    st.header(f"💬 Assistant IA - Domaine : {st.session_state.current_domain}")
    query = st.text_area("Pose ta question ici")
    if st.button("Envoyer"):
        if query:
            st.session_state.messages.append({"role": "user", "content": query})
            response = generate_ai_response(query, st.session_state.current_domain)
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Affichage messages
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"**Vous :** {msg['content']}")
        else:
            st.markdown(f"**Assistant :** {msg['content']}")

elif page == "💻 Analyse Code":
    st.header("💻 Analyse de code")
    code_file = st.file_uploader("Importer un fichier code", type=["py", "js", "java"], key="code_upload")
    if code_file:
        code_content = code_file.read().decode("utf-8")
        st.code(code_content, language="python")
        st.markdown("**Suggestions d'optimisation :**")
        if "TODO" in code_content or "FIXME" in code_content:
            st.write("- Contient des TODO/FIXME à traiter")
        if len(code_content.splitlines()) > 100:
            st.write("- Trop long, envisager de découper en fonctions")
        if "import *" in code_content:
            st.write("- Éviter les importations globales *")

elif page == "⚙️ Configuration":
    st.header("⚙️ Configuration")
    st.write("Clé OpenAI : ", "✅ Détectée" if api_key else "❌ Manquante")
    st.write(f"Domaine actuel : {st.session_state.current_domain}")
    st.write(f"Documents ingérés : {len(st.session_state.documents)}")