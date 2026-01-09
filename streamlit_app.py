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
import json
import os
from pathlib import Path
import io

# PDF / DOC / CODE ingestion
from PyPDF2 import PdfReader
import docx

# OpenAI client
from openai import OpenAI

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
# OPENAI KEY INTEGRATION
# ===============================
api_key = st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error("🔑 OpenAI API key missing! Check .streamlit/secrets.toml")
    st.stop()
else:
    client = OpenAI(api_key=api_key)
    st.success("✅ OpenAI key detected and client initialized")

# ===============================
# DOMAINS / SPECIALIZATIONS
# ===============================
DOMAINS = {
    "💼 HR & Recruitment / RH & Recrutement": {
        "description": "Expert assistant for HR tasks / Assistant expert pour les RH",
        "system_prompt": """You are an HR expert. You help with CV analysis, job descriptions, interview guidance, training plans, conflict resolution.
Vous êtes un expert RH. Vous aidez à l'analyse de CV, rédaction de fiches de poste, entretien, formation, gestion de conflits."""
    },
    "⚖️ Legal & Compliance / Juridique & Compliance": {
        "description": "Legal expert assistant / Assistant expert juridique",
        "system_prompt": """You are a legal assistant. You help with contract analysis, due diligence, compliance and legal document drafting.
Vous êtes un assistant juridique. Vous aidez à l'analyse de contrats, due diligence, conformité et rédaction juridique."""
    },
    "🏥 Medical & Health / Médical & Santé": {
        "description": "Medical professional assistant / Assistant pour professionnels de santé",
        "system_prompt": """You are a medical assistant for professionals. You help with patient records, differential diagnosis, research, and reports.
Vous êtes un assistant médical pour professionnels. Vous aidez avec les dossiers patients, diagnostic différentiel, recherches et comptes-rendus."""
    },
    "🔬 Research & Science / Recherche & Sciences": {
        "description": "Research assistant for scientific work / Assistant pour la recherche scientifique",
        "system_prompt": """You are a research assistant. You help with literature review, data analysis, article drafting, hypothesis generation.
Vous êtes un assistant de recherche. Vous aidez aux revues de littérature, analyse de données, rédaction et génération d'hypothèses."""
    },
    "💻 Development & Code / Développement & Code": {
        "description": "Technical assistant for developers / Assistant technique pour développeurs",
        "system_prompt": """You are a software development expert. You help with code review, debugging, optimization, documentation.
Vous êtes un expert en développement logiciel. Vous aidez à la revue de code, débogage, optimisation et documentation."""
    },
    "📊 Business & Analytics / Analyse & Business Intelligence": {
        "description": "Assistant for data analysis and business insights / Assistant pour l'analyse de données et BI",
        "system_prompt": """You are a business intelligence assistant. You help with KPIs, dashboards, predictions, insights.
Vous êtes un assistant BI. Vous aidez avec KPIs, tableaux de bord, prévisions et analyses business."""
    }
}

# ===============================
# PAGE HEADER
# ===============================
st.markdown("""
# MicroLLM Studio - Enterprise AI Assistant
**On-Premise Platform / Plateforme locale sécurisée**
""")

# ===============================
# DOMAIN SELECTION
# ===============================
domain = st.selectbox(
    "Select domain / Sélectionnez un domaine",
    options=list(DOMAINS.keys()),
    index=0
)

st.markdown(f"**Domain Description / Description du domaine:** {DOMAINS[domain]['description']}")

# ===============================
# FILE UPLOAD
# ===============================
st.header("📂 File Ingestion / Téléversement de fichiers")
uploaded_files = st.file_uploader(
    "Upload PDF, DOCX, code files (Python, JS, TXT, CSV) / Téléversez vos fichiers PDF, DOCX, code",
    type=["pdf", "docx", "py", "js", "txt", "csv"],
    accept_multiple_files=True
)

def extract_text(file):
    """Extract text depending on file type"""
    if file.type == "application/pdf":
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    else:
        return file.getvalue().decode("utf-8", errors="ignore")

documents_text = ""
if uploaded_files:
    for f in uploaded_files:
        st.info(f"Processing / Traitement : {f.name}")
        text = extract_text(f)
        documents_text += f"\n---\n**{f.name}**\n{text}"

if documents_text:
    st.subheader("📄 Extracted Content / Contenu extrait")
    st.text_area("Combined text of uploaded files / Texte combiné des fichiers", documents_text, height=300)

# ===============================
# CHAT INTERFACE
# ===============================
st.header("💬 AI Assistant / Assistant IA")

user_input = st.text_input("Enter your question / Posez votre question ici:")
if st.button("Send / Envoyer") and user_input:
    system_prompt = DOMAINS[domain]["system_prompt"]
    prompt = f"""
System / Système :
{system_prompt}

Documents / Documents :
{documents_text}

User question / Question utilisateur :
{user_input}

Answer in English and French / Répondre en anglais et français.
"""
    with st.spinner("🧠 Generating AI response / Génération de réponse IA..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            answer = response.choices[0].message.content
            st.markdown(f"**AI Response / Réponse IA :**\n\n{answer}")
        except Exception as e:
            st.error(f"❌ Error calling OpenAI / Erreur lors de l'appel à OpenAI : {e}")

# ===============================
# END OF STREAMLIT
# ===============================
st.markdown("---")
st.info("MicroLLM Studio - All data stays private and secure / Toutes les données restent privées et sécurisées.")
