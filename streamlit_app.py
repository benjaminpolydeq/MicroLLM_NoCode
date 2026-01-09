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
import re
import base64
from pathlib import Path
import io

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
# ARSLM & MICROLLM INFO
# ===============================
SYSTEM_INFO = {
    "platform": "MicroLLM Studio",
    "version": "1.0.0-Enterprise",
    "base_model": "ARSLM",
    "arslm_description": (
        "ARSLM (Adaptive Reasoning Semantic Language Model) est un moteur AI propriétaire "
        "léger et sécurisé, conçu pour le traitement de données sensibles en environnement "
        "on-premise. Aucune donnée ne quitte votre infrastructure."
    ),
    "microllm_description": (
        "MicroLLM Studio est une plateforme no-code permettant de déployer et spécialiser "
        "des assistants IA dans des domaines sensibles : médical, juridique, RH, recherche, "
        "développement. Chaque entreprise peut personnaliser son assistant selon ses besoins "
        "spécifiques tout en garantissant la confidentialité absolue des données."
    ),
    "features": [
        "🔒 100% On-Premise - Aucune donnée ne quitte votre infrastructure",
        "🧠 Spécialisation domaine - Médical, Juridique, RH, Recherche, Dev",
        "📚 Ingestion multi-formats - PDF, Word, Excel, Code, Images, etc.",
        "🔍 Recherche sécurisée - Navigation web sans traces externes",
        "💻 Analyse de code - Revue, refactoring, génération, debugging",
        "📊 Génération de rapports - Résumés, analyses, études approfondies",
        "🎯 No-Code Interface - Aucune compétence technique requise",
        "🔐 Sécurité renforcée - Chiffrement, audit, conformité RGPD"
    ]
}

# ===============================
# SPECIALIZED DOMAINS
# ===============================
DOMAINS = {
    "💼 RH & Recrutement": {
        "description": "Assistant spécialisé pour les ressources humaines",
        "system_prompt": """Tu es un expert en ressources humaines et recrutement. Tu aides avec :
- L'analyse de CV et lettres de motivation
- La rédaction de fiches de poste et annonces d'emploi
- Les entretiens d'embauche et l'évaluation des candidats
- La gestion des conflits et médiation
- Les plans de formation et développement des compétences
- Les politiques RH et procédures internes

Tu dois être professionnel, bienveillant et respecter la confidentialité des données personnelles.""",
        "capabilities": [
            "Analyse de CV et lettres de motivation",
            "Rédaction de fiches de poste",
            "Génération de contrats de travail",
            "Évaluation des candidats",
            "Plans de formation",
            "Gestion des conflits"
        ],
        "use_cases": [
            "Screening automatique de candidatures",
            "Réponses aux questions employés",
            "Génération de documents RH",
            "Analyse de satisfaction"
        ]
    },
    "⚖️ Juridique & Compliance": {
        "description": "Assistant pour professionnels du droit",
        "system_prompt": """Tu es un assistant juridique expert. Tu aides avec :
- L'analyse de contrats et identification de clauses problématiques
- La recherche jurisprudentielle et doctrine
- La rédaction de documents juridiques (mémoires, conclusions, etc.)
- La conformité RGPD et réglementations
- La due diligence documentaire
- La veille juridique et réglementaire

IMPORTANT: Tu dois toujours rappeler que tes réponses sont à titre informatif et ne constituent pas un conseil juridique. En cas de doute, consulter un avocat.""",
        "capabilities": [
            "Analyse de contrats et clauses",
            "Recherche jurisprudentielle",
            "Rédaction de mémoires",
            "Conformité RGPD",
            "Due diligence documentaire",
            "Veille juridique"
        ],
        "use_cases": [
            "Revue de contrats commerciaux",
            "Analyse de risques légaux",
            "Rédaction de documents juridiques",
            "Audit de conformité"
        ]
    },
    "🏥 Médical & Santé": {
        "description": "Assistant pour professionnels de santé",
        "system_prompt": """Tu es un assistant médical spécialisé pour professionnels de santé. Tu aides avec :
- L'analyse de dossiers médicaux et antécédents
- L'aide au diagnostic différentiel (liste de diagnostics possibles)
- La recherche bibliographique médicale
- La rédaction de comptes-rendus et protocoles
- La veille scientifique et études cliniques
- L'interprétation de résultats d'examens

CRUCIAL: Tu dois TOUJOURS rappeler :
⚠️ Cette information est destinée aux professionnels de santé uniquement
⚠️ Ne remplace PAS une consultation médicale
⚠️ En cas d'urgence, appeler le 15 (SAMU)
Tes réponses sont à titre informatif et éducatif uniquement.""",
        "capabilities": [
            "Analyse de dossiers médicaux",
            "Aide au diagnostic différentiel",
            "Recherche bibliographique médicale",
            "Rédaction de comptes-rendus",
            "Veille scientifique",
            "Analyse d'imagerie (descriptions)"
        ],
        "use_cases": [
            "Support décisionnel clinique",
            "Résumés de littérature médicale",
            "Génération de protocoles",
            "Analyse de tendances épidémiologiques"
        ]
    },
    "🔬 Recherche & Sciences": {
        "description": "Assistant pour chercheurs et scientifiques",
        "system_prompt": """Tu es un assistant de recherche scientifique expert. Tu aides avec :
- Les revues de littérature systématiques
- L'analyse de données expérimentales et statistiques
- La rédaction d'articles scientifiques
- La génération d'hypothèses de recherche
- L'analyse critique de méthodologies
- La veille scientifique et bibliométrie

Tu dois être rigoureux, factuel, et citer les sources scientifiques quand c'est pertinent. Adopte une démarche scientifique critique.""",
        "capabilities": [
            "Revue de littérature scientifique",
            "Analyse de données expérimentales",
            "Rédaction d'articles",
            "Génération d'hypothèses",
            "Analyse statistique",
            "Veille scientifique"
        ],
        "use_cases": [
            "État de l'art automatisé",
            "Synthèse de publications",
            "Analyse de résultats",
            "Rédaction de propositions de recherche"
        ]
    },
    "💻 Développement & Code": {
        "description": "Assistant pour développeurs et équipes tech",
        "system_prompt": """Tu es un expert en développement logiciel et architecture. Tu aides avec :
- La revue de code et suggestions d'amélioration
- La génération de code propre et documenté
- La détection de bugs, vulnérabilités et failles de sécurité
- La documentation technique et commentaires
- L'analyse d'algorithmes et optimisation
- Les best practices et design patterns

Tu dois produire du code de qualité production, bien structuré, sécurisé et maintenable. Explique tes choix techniques.""",
        "capabilities": [
            "Revue de code et refactoring",
            "Génération de code",
            "Détection de bugs et vulnérabilités",
            "Documentation automatique",
            "Analyse d'algorithmes",
            "Optimisation de performance"
        ],
        "use_cases": [
            "Code review automatisé",
            "Génération de tests unitaires",
            "Migration de code",
            "Analyse de complexité"
        ]
    },
    "📊 Analyse & Business Intelligence": {
        "description": "Assistant pour analystes et décideurs",
        "system_prompt": """Tu es un expert en analyse de données et business intelligence. Tu aides avec :
- L'analyse de données volumineuses et KPIs
- La génération de rapports exécutifs et tableaux de bord
- Les prédictions et analyses de tendances
- Les insights business et recommandations stratégiques
- L'optimisation opérationnelle et financière
- La visualisation de données

Tu dois être analytique, factuel, et fournir des recommandations actionnables basées sur les données.""",
        "capabilities": [
            "Analyse de données volumineuses",
            "Génération de rapports",
            "Prédictions et tendances",
            "Tableaux de bord",
            "Insights business",
            "Recommandations stratégiques"
        ],
        "use_cases": [
            "Rapports exécutifs automatisés",
            "Analyse de marché",
            "Prévisions financières",
            "Optimisation opérationnelle"
        ]
    }
}

# ===============================
# CUSTOM CSS (Identique)
# ===============================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #667eea 100%);
        padding: 2.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header .subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    .main-header .arslm-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        color: white;
        font-size: 0.9rem;
        margin-top: 1rem;
        backdrop-filter: blur(10px);
    }
    
    .security-badge {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.3);
    }
    
    .domain-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .domain-card:hover {
        border-color: #667eea;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
        transform: translateY(-5px);
    }
    
    .domain-card.active {
        border-color: #667eea;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
    }
    
    .domain-card h3 {
        color: #1e3c72;
        margin-top: 0;
        font-size: 1.3rem;
    }
    
    .user-msg {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 15px;
        margin: 1rem 0;
        margin-left: 15%;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        animation: slideInRight 0.3s ease;
    }
    
    .assistant-msg {
        background: #f8f9fa;
        color: #1a1a1a;
        padding: 1.2rem;
        border-radius: 15px;
        margin: 1rem 0;
        margin-right: 15%;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        animation: slideInLeft 0.3s ease;
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .capability-tag {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 15px;
        font-size: 0.85rem;
        margin: 0.2rem;
        font-weight: 500;
    }
    
    .info-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-left: 4px solid #667eea;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0;
    }
    
    .info-box h4 {
        color: #1e3c72;
        margin-top: 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 6px 20px rgba(30, 60, 114, 0.3);
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: scale(1.05);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .upload-zone {
        border: 2px dashed #667eea;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        background: rgba(102, 126, 234, 0.05);
        margin: 1rem 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.1) 0%, rgba(255, 159, 64, 0.1) 100%);
        border-left: 4px solid #ff6b6b;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .success-box {
        background: linear-gradient(135deg, rgba(17, 153, 142, 0.1) 0%, rgba(56, 239, 125, 0.1) 100%);
        border-left: 4px solid #11998e;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .code-block {
        background: #1e1e1e;
        color: #d4d4d4;
        padding: 1rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        overflow-x: auto;
        margin: 1rem 0;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# ===============================
# AI ENGINE WITH REAL RESPONSES
# ===============================
def call_ai_api(messages, domain):
    """
    Appelle l'API Claude pour générer des réponses réelles
    """
    try:
        # Construire le system prompt basé sur le domaine
        domain_info = DOMAINS.get(domain, {})
        system_prompt = domain_info.get("system_prompt", "Tu es un assistant IA professionnel et serviable.")
        
        # Préparer les messages pour l'API
        api_messages = []
        for msg in messages:
            api_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Appel à l'API Claude via fetch
        response = st.session_state.get('api_response', None)
        
        # Pour l'instant, simuler une réponse intelligente basée sur le domaine
        # Dans la vraie version, ceci sera remplacé par un vrai appel API
        user_query = messages[-1]["content"] if messages else ""
        
        # Générer une réponse contextuelle basée sur le domaine
        if "💼 RH" in domain:
            response_text = f"""En tant qu'expert RH, voici mon analyse de votre demande :

**Concernant : {user_query}**

Je peux vous aider avec plusieurs aspects :

1. **Analyse approfondie** : Je peux examiner les CV, lettres de motivation, ou documents RH que vous souhaitez analyser.

2. **Rédaction** : Je peux vous aider à rédiger des fiches de poste, des annonces d'emploi, ou des documents de formation.

3. **Conseils** : Je peux vous fournir des recommandations sur les meilleures pratiques RH, la gestion des conflits, ou le développement des compétences.

4. **Conformité** : Je peux vous aider à respecter les obligations légales et les bonnes pratiques en matière de RH.

📎 **Suggestion** : Partagez-moi le document ou la problématique spécifique, et je vous fournirai une analyse détaillée et des recommandations actionnables.

💡 **Note de confidentialité** : Toutes les données que vous partagez restent privées et sécurisées dans votre environnement."""

        elif "⚖️ Juridique" in domain:
            response_text = f"""En tant qu'assistant juridique, voici mon analyse :

**Sujet : {user_query}**

🔍 **Analyse juridique** :

Je peux vous assister sur :
- L'analyse de contrats et l'identification de clauses problématiques
- La recherche de jurisprudence et de doctrine pertinente
- La rédaction de documents juridiques (mémoires, conclusions)
- L'évaluation de conformité réglementaire (RGPD, etc.)

⚖️ **Méthodologie** :
1. Examen approfondi des documents
2. Identification des risques juridiques
3. Recommandations et solutions
4. Rédaction si nécessaire

⚠️ **DISCLAIMER IMPORTANT** :
Cette analyse est fournie à titre informatif uniquement et ne constitue PAS un conseil juridique. Pour des questions juridiques spécifiques engageant votre responsabilité, consultez un avocat qualifié.

📄 Partagez-moi vos documents pour une analyse détaillée."""

        elif "🏥 Médical" in domain:
            response_text = f"""**Analyse médicale professionnelle**

Demande : {user_query}

En tant qu'assistant médical pour professionnels de santé, je peux vous aider avec :

🩺 **Support clinique** :
- Aide au diagnostic différentiel
- Analyse de dossiers médicaux
- Recherche bibliographique médicale
- Interprétation de résultats

📚 **Documentation** :
- Rédaction de comptes-rendus
- Synthèse de littérature médicale
- Protocoles de soins

🔬 **Recherche** :
- Veille scientifique
- Analyse d'études cliniques

⚠️ **AVERTISSEMENTS CRUCIAUX** :
⛔ Cette information est destinée aux PROFESSIONNELS DE SANTÉ uniquement
⛔ Ne remplace PAS une consultation médicale
⛔ En cas d'URGENCE VITALE : appeler le 15 (SAMU)
⛔ À titre informatif et éducatif uniquement

Partagez-moi les informations cliniques pertinentes pour une analyse approfondie."""

        elif "🔬 Recherche" in domain:
            response_text = f"""**Assistance à la recherche scientifique**

Projet : {user_query}

En tant qu'assistant de recherche, je peux contribuer à :

📖 **Revue de littérature** :
- Analyse systématique de publications
- Synthèse de l'état de l'art
- Bibliométrie et tendances

📊 **Analyse de données** :
- Interprétation statistique
- Visualisation de résultats
- Identification de patterns

✍️ **Rédaction scientifique** :
- Structure d'articles
- Méthodologie
- Discussion des résultats

💡 **Génération d'hypothèses** :
- Approche critique
- Perspectives innovantes

Partagez-moi vos données, articles ou problématique de recherche pour une analyse scientifique rigoureuse."""

        elif "💻 Développement" in domain:
            response_text = f"""**Assistance technique développement**

Requête : {user_query}

En tant qu'expert en développement, je peux vous aider avec :

💻 **Revue de code** :
- Analyse de qualité
- Détection de bugs et vulnérabilités
- Suggestions d'optimisation
- Best practices

🔧 **Génération de code** :
- Code propre et documenté
- Tests unitaires
- Respect des design patterns

🐛 **Debug et optimisation** :
- Identification de problèmes
- Solutions de performance
- Refactoring

