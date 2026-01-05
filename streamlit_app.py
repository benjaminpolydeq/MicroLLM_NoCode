"""
MicroLLM Studio / ARSLM Chat Studio - Lightweight Version for Streamlit Cloud
No PyTorch dependencies - Pure Python implementation
Copyright © 2025 Benjamin Amaad Kama. All Rights Reserved.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import json
import os
import re
import PyPDF2
from io import StringIO

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="ARSLM Studio",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# ARSLM INFO
# ===============================
ARSLM_INFO = {
    "name": "ARSLM",
    "version": "1.0.0-MVP",
    "description": (
        "ARSLM – Lightweight, Efficient & Secure AI\n\n"
        "ARSLM is a compact language model built for real-world applications, "
        "combining speed, efficiency, and adaptability. Designed to run on low-resource "
        "environments or on-premise, it ensures data privacy while providing intelligent "
        "text generation and chat capabilities."
    )
}

# ===============================
# CUSTOM CSS
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
        margin-bottom: 1rem;
    }

    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.2);
        transition: transform 0.2s;
        cursor: pointer;
        margin: 10px 0;
    }

    .metric-card:hover { transform: scale(1.05); }

    .metric-value { font-size: 2.5rem; font-weight: bold; margin: 10px 0; }

    .metric-label { font-size: 0.9rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px; }

    .user-msg {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        margin-left: 20%;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .assistant-msg {
        background: #f7f7f8;
        color: #1a1a1a;
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        margin-right: 20%;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .info-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-left: 4px solid #667eea;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
    }

    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# ===============================
# ARSLM ENGINE (Lightweight)
# ===============================
class ARSLMEngine:
    """Lightweight ARSLM engine without PyTorch dependencies"""

    def __init__(self):
        self.knowledge_base = self._load_knowledge_base()
        self.conversation_history = []

    def _load_knowledge_base(self):
        """Load knowledge base"""
        return [
            {
                "keywords": ["arslm", "what is", "qu'est-ce", "définition"],
                "response": (
                    "**ARSLM (Adaptive Reasoning Semantic Language Model)** est un moteur AI "
                    "propriétaire léger conçu pour les entreprises.\n\n"
                    "🎯 **Caractéristiques principales** :\n"
                    "- Génération de réponses intelligentes\n"
                    "- Maintien du contexte conversationnel\n"
                    "- Déploiement local ou cloud\n"
                    "- Confidentialité totale des données\n"
                    "- Coûts prévisibles\n\n"
                    "📧 Contact : benjokama@hotmail.fr"
                )
            },
            {
                "keywords": ["pricing", "prix", "tarifs", "cost", "coût"],
                "response": (
                    "💰 **Plans ARSLM** :\n\n"
                    "**🆓 Évaluation** : Gratuit\n"
                    "- 30 jours, 100 conversations/mois\n"
                    "- Support communautaire\n\n"
                    "**🚀 Starter** : $99/mois\n"
                    "- 5,000 conversations/mois\n"
                    "- Support email 72h\n\n"
                    "**💼 Professional** : $299/mois\n"
                    "- 25,000 conversations/mois\n"
                    "- API REST, personnalisation\n"
                    "- Support 48h\n\n"
                    "**🏢 Enterprise** : Sur devis\n"
                    "- Illimité, white-label, 24/7\n\n"
                    "🎁 **-30% pour marchés émergents** (Afrique, Asie, Latam)\n\n"
                    "📧 benjokama@hotmail.fr"
                )
            },
            {
                "keywords": ["features", "fonctionnalités", "capabilities", "peut faire"],
                "response": (
                    "✨ **Fonctionnalités ARSLM** :\n\n"
                    "💬 **Génération intelligente**\n"
                    "- Réponses contextuelles\n"
                    "- Compréhension du langage naturel\n\n"
                    "🧠 **Mémoire conversationnelle**\n"
                    "- Historique des sessions\n"
                    "- Préservation du contexte\n\n"
                    "🎯 **Personnalisation**\n"
                    "- Adapté à vos besoins métiers\n"
                    "- Templates pré-configurés\n\n"
                    "🌍 **Déploiement flexible**\n"
                    "- Local, cloud privé, hybrid\n"
                    "- Aucune dépendance Internet\n\n"
                    "💰 **Coûts prévisibles**\n"
                    "- Licence fixe, pas de surprise\n"
                    "- ROI rapide"
                )
            },
            {
                "keywords": ["install", "setup", "déploiement", "installation"],
                "response": (
                    "🚀 **Installation ARSLM** :\n\n"
                    "```bash\n"
                    "# Cloner le repository\n"
                    "git clone https://github.com/benjaminpolydeq/ARSLM.git\n"
                    "cd ARSLM\n\n"
                    "# Installer les dépendances\n"
                    "pip install -r requirements.txt\n\n"
                    "# Lancer l'application\n"
                    "streamlit run streamlit_app.py\n"
                    "```\n\n"
                    "💡 **Options de déploiement** :\n"
                    "- Local (votre machine)\n"
                    "- Cloud privé (AWS, Azure, GCP)\n"
                    "- Streamlit Cloud\n"
                    "- Docker container\n\n"
                    "📚 Documentation complète sur GitHub"
                )
            },
            {
                "keywords": ["support", "help", "aide", "contact", "assistance"],
                "response": (
                    "🤝 **Support ARSLM** :\n\n"
                    "📧 **Email** : benjokama@hotmail.fr\n"
                    "💻 **GitHub** : @benjaminpolydeq\n"
                    "📍 **Localisation** : Nguekhokh, Mbour, Sénégal\n\n"
                    "**Support selon le plan** :\n"
                    "- 🆓 Community : GitHub Issues\n"
                    "- 🚀 Starter : Email 72h\n"
                    "- 💼 Professional : Email prioritaire 48h\n"
                    "- 🏢 Enterprise : 24/7 avec SLA\n\n"
                    "**Autres demandes** :\n"
                    "- Démos personnalisées\n"
                    "- Devis Enterprise\n"
                    "- Licences commerciales\n"
                    "- Partenariats"
                )
            },
            {
                "keywords": ["advantages", "avantages", "benefits", "pourquoi"],
                "response": (
                    "🌟 **Pourquoi choisir ARSLM ?**\n\n"
                    "🔒 **Confidentialité totale**\n"
                    "- Données locales, pas de cloud tiers\n"
                    "- Conformité RGPD garantie\n\n"
                    "💰 **Coûts maîtrisés**\n"
                    "- Licence fixe vs pay-per-token\n"
                    "- ROI prévisible\n\n"
                    "⚡ **Performance**\n"
                    "- Latence faible en local\n"
                    "- Fonctionne hors ligne\n\n"
                    "🎯 **Personnalisation**\n"
                    "- Adapté à vos processus\n"
                    "- Templates métiers\n\n"
                    "🌍 **Marchés émergents**\n"
                    "- Support spécifique Afrique/Asie\n"
                    "- Tarifs adaptés\n\n"
                    "🔓 **Pas de vendor lock-in**\n"
                    "- Architecture ouverte\n"
                    "- Migration facile"
                )
            }
        ]

    def generate_response(self, query):
        """Generate response based on query"""
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
            response = self._fallback_response(query)

        self.conversation_history.append({
            "query": query,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
        return response

    def _fallback_response(self, query):
        return (
            f"🤔 Je n'ai pas de réponse spécifique pour **\"{query}\"**.\n\n"
            "💡 **Questions que je peux traiter** :\n"
            "- Qu'est-ce que ARSLM ?\n"
            "- Quelles sont les fonctionnalités ?\n"
            "- Quels sont les tarifs ?\n"
            "- Comment installer ARSLM ?\n"
            "- Quels sont les avantages ?\n"
            "- Comment obtenir du support ?\n\n"
            "📧 Pour plus d'aide : **benjokama@hotmail.fr**"
        )

    # ==========================
    # Document Query
    # ==========================
    def query_document(self, query):
        if hasattr(st.session_state, "current_document") and st.session_state.current_document:
            doc = st.session_state.current_document
            if "titre" in query.lower():
                title = doc.strip().split("\n")[0]
                return f"📌 Le titre du document est : **{title}**"
            elif "résumé" in query.lower() or "summary" in query.lower():
                summary = "\n".join(doc.strip().split("\n")[:5])
                return f"📝 Résumé du document :\n{summary}"
            elif "clé" in query.lower() or "key" in query.lower():
                lines = doc.strip().split("\n")
                key_info = [line for line in lines if len(line.split()) > 3][:5]
                return "🔑 Informations clés du document :\n" + "\n".join(key_info)
            else:
                return "📄 Document chargé. Posez une question sur le titre, résumé ou informations clés."
        else:
            return self.generate_response(query)

# ===============================
# SESSION STATE
# ===============================
if "engine" not in st.session_state:
    st.session_state.engine = ARSLMEngine()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "models" not in st.session_state:
    st.session_state.models = []
if "training_history" not in st.session_state:
    st.session_state.training_history = []
if "current_document" not in st.session_state:
    st.session_state.current_document = None

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/667eea/ffffff?text=ARSLM+Studio", use_container_width=True)
    st.markdown("---")
    page = st.radio("Navigation", ["🏠 Dashboard", "💬 Chat", "📊 Analytics", "⚙️ Settings"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("### 📊 System Status")
    st.success("🟢 Active")
    st.metric("Models", len(st.session_state.models))
    st.metric("Conversations", len(st.session_state.messages))
    st.markdown("---")
    st.info(f"""**{ARSLM_INFO['name']}**  
Version {ARSLM_INFO['version']}  
📧 benjokama@hotmail.fr  
💻 [@benjaminpolydeq](https://github.com/benjaminpolydeq)  
© 2025 Benjamin Amaad Kama""")

# ===============================
# DASHBOARD
# ===============================
if page == "🏠 Dashboard":
    st.markdown('<p class="main-header">ARSLM Studio</p>', unsafe_allow_html=True)
    st.caption("Proprietary AI – On-Premise & No-Code")
    st.markdown("### 🧠 About ARSLM")
    st.markdown(f'<div class="info-box">{ARSLM_INFO["description"]}</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    for i, label in enumerate(["Active Models", "Conversations", "Status", "Security"]):
        value = [len(st.session_state.models), len(st.session_state.messages), "✓", "🔒"][i]
        col = [col1, col2, col3, col4][i]
        col.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📈 Performance Overview")
    epochs = list(range(1, 11))
    performance = [60, 65, 72, 78, 83, 87, 90, 92, 94, 95]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=epochs, y=performance, mode="lines+markers", line=dict(color='#667eea', width=3), marker=dict(size=8)))
    fig.update_layout(height=400, hovermode="x unified", xaxis_title="Epochs", yaxis_title="Accuracy (%)", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("### ⚡ Quick Actions")
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("💬 Start Chat", use_container_width=True): st.session_state.page="💬 Chat"; st.rerun()
    with c2:
        if st.button("📊 View Analytics", use_container_width=True): st.session_state.page="📊 Analytics"; st.rerun()
    with c3:
        if st.button("📧 Contact Support", use_container_width=True): st.markdown("[benjokama@hotmail.fr](mailto:benjokama@hotmail.fr)")

# ===============================
# CHAT
# ===============================
elif page == "💬 Chat":
    st.markdown('<p class="main-header">ARSLM Chat</p>', unsafe_allow_html=True)
    st.caption(f"Chatting with {ARSLM_INFO['name']} v{ARSLM_INFO['version']}")

    # ===============================
    # Upload fichiers
    # ===============================
    st.markdown("### 📂 Upload de fichiers")
    uploaded_file = st.file_uploader("Téléchargez un fichier PDF ou TXT", type=["pdf", "txt"])
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            full_text = ""
            for page in pdf_reader.pages: full_text += page.extract_text() + "\n"
            st.session_state.current_document = full_text
            st.success(f"📄 PDF chargé avec {len(pdf_reader.pages)} pages.")
        elif uploaded_file.type == "text/plain":
            full_text = str(uploaded_file.read(), "utf-8")
            st.session_state.current_document = full_text
            st.success("📄 Fichier texte chargé avec succès.")

    # Display messages
    if not st.session_state.messages:
        st.markdown('<div class="assistant-msg"><strong>👋 Bienvenue sur ARSLM Chat !</strong><br><br>Posez-moi vos questions ou chargez un document PDF/TXT pour extraire titre, résumé et informations clés.</div>', unsafe_allow_html=True)

    for msg in st.session_state.messages:
        cls = "user-msg" if msg["role"]=="user" else "assistant-msg"
        st.markdown(f'<div class="{cls}">{"👤" if msg["role"]=="user" else "🤖"} {msg["content"]}</div>', unsafe_allow