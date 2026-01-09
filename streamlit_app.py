"""
MicroLLM Studio - Enterprise On-Premise AI Assistant
Built on ARSLM - Secure, Private, Specialized AI for Sensitive Domains

Copyright © 2025 Benjamin Amaad Kama.
All Rights Reserved.
Proprietary Software - License Required for Commercial Use
"""

import streamlit as st
from datetime import datetime

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="MicroLLM Studio - Enterprise AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# SYSTEM INFO
# ==================================================
SYSTEM_INFO = {
    "platform": "MicroLLM Studio",
    "version": "1.0.0-Enterprise",
    "base_model": "ARSLM",
}

# ==================================================
# DOMAINS
# ==================================================
DOMAINS = {
    "💼 RH & Recrutement": {
        "system_prompt": "Expert RH et recrutement."
    },
    "⚖️ Juridique & Compliance": {
        "system_prompt": "Assistant juridique expert (informatif uniquement)."
    },
    "🏥 Médical & Santé": {
        "system_prompt": "Assistant médical pour professionnels de santé."
    },
    "🔬 Recherche & Sciences": {
        "system_prompt": "Assistant de recherche scientifique."
    },
    "💻 Développement & Code": {
        "system_prompt": "Expert développement logiciel et architecture."
    },
    "📊 Analyse & Business Intelligence": {
        "system_prompt": "Expert data et business intelligence."
    }
}

# ==================================================
# SESSION STATE
# ==================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "domain" not in st.session_state:
    st.session_state.domain = "💻 Développement & Code"

# ==================================================
# HEADER
# ==================================================
st.markdown(
    f"""
    <div style="background:linear-gradient(135deg,#1e3c72,#667eea);
                padding:2rem;border-radius:15px;color:white;">
        <h1>🤖 {SYSTEM_INFO['platform']}</h1>
        <p>Built on {SYSTEM_INFO['base_model']} — Enterprise On-Premise AI</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ==================================================
# SIDEBAR
# ==================================================
with st.sidebar:
    st.markdown("## 🎯 Domaine de spécialisation")
    st.session_state.domain = st.selectbox(
        "Choisir un domaine",
        list(DOMAINS.keys())
    )

    st.markdown("---")
    st.markdown("🔐 **100% On-Premise — Confidentialité Totale**")

# ==================================================
# AI RESPONSE ENGINE (SAFE)
# ==================================================
def generate_response(user_query: str, domain: str) -> str:
    if "💼 RH" in domain:
        return (
            "**Analyse RH Professionnelle**\n\n"
            f"Demande : {user_query}\n\n"
            "- Analyse de CV et profils\n"
            "- Rédaction de documents RH\n"
            "- Recommandations pratiques\n\n"
            "📌 Les données restent strictement confidentielles."
        )

    if "⚖️ Juridique" in domain:
        return (
            "**Analyse Juridique (Informationnelle)**\n\n"
            f"Sujet : {user_query}\n\n"
            "- Analyse de contrats\n"
            "- Identification de risques\n"
            "- Conformité réglementaire\n\n"
            "⚠️ Ceci ne constitue pas un conseil juridique."
        )

    if "🏥 Médical" in domain:
        return (
            "**Analyse Médicale Professionnelle**\n\n"
            f"Demande : {user_query}\n\n"
            "- Support au diagnostic différentiel\n"
            "- Analyse documentaire médicale\n"
            "- Veille scientifique\n\n"
            "⚠️ Réservé aux professionnels de santé."
        )

    if "🔬 Recherche" in domain:
        return (
            "**Assistance à la Recherche Scientifique**\n\n"
            f"Projet : {user_query}\n\n"
            "- Revue de littérature\n"
            "- Analyse méthodologique\n"
            "- Rédaction scientifique\n"
        )

    if "💻 Développement" in domain:
        return (
            "**Assistance Technique Développement**\n\n"
            f"Requête : {user_query}\n\n"
            "💻 Revue de code\n"
            "- Qualité et lisibilité\n"
            "- Détection de bugs\n"
            "- Sécurité et performance\n\n"
            "🔧 Génération & Refactoring\n"
            "- Code production-ready\n"
            "- Tests unitaires\n"
            "- Design patterns\n\n"
            "🔐 Tout reste en environnement on-premise."
        )

    if "📊 Analyse" in domain:
        return (
            "**Analyse & Business Intelligence**\n\n"
            f"Question : {user_query}\n\n"
            "- Analyse de données\n"
            "- KPIs & reporting\n"
            "- Recommandations stratégiques"
        )

    return "Assistant prêt à vous aider."

# ==================================================
# CHAT UI
# ==================================================
st.markdown("## 💬 Assistant IA")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Posez votre question…")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    response = generate_response(user_input, st.session_state.domain)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()

# ==================================================
# FOOTER
# ==================================================
st.markdown(
    f"""
    <hr>
    <small>
    © 2025 Benjamin Amaad Kama — MicroLLM Studio — {SYSTEM_INFO['version']}
    </small>
    """,
    unsafe_allow_html=True
)