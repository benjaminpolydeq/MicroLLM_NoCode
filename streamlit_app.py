# -*- coding: utf-8 -*-
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

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="MicroLLM Studio - Enterprise AI",
    page_icon="\U0001F916",  # 🤖
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# SYSTEM INFO
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
        "\U0001F512 100% On-Premise - Aucune donnée ne quitte votre infrastructure",  # 🔒
        "\U0001F9E0 Spécialisation domaine - Médical, Juridique, RH, Recherche, Dev",  # 🧠
        "\U0001F4DA Ingestion multi-formats - PDF, Word, Excel, Code, Images, etc.",  # 📚
        "\U0001F50D Recherche sécurisée - Navigation web sans traces externes",  # 🔍
        "\U0001F4BB Analyse de code - Revue, refactoring, génération, debugging",  # 💻
        "\U0001F4CA Génération de rapports - Résumés, analyses, études approfondies",  # 📊
        "\U0001F3AF No-Code Interface - Aucune compétence technique requise",  # 🎯
        "\U0001F510 Sécurité renforcée - Chiffrement, audit, conformité RGPD"  # 🔐
    ]
}

# ===============================
# DOMAINS
# ===============================
DOMAINS = {
    "\U0001F4BC RH & Recrutement": {  # 💼
        "description": "Assistant spécialisé pour les ressources humaines",
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
    "\u2696\ufe0f Juridique & Compliance": {  # ⚖️
        "description": "Assistant pour professionnels du droit",
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
    "\U0001F3E5 Médical & Santé": {  # 🏥
        "description": "Assistant pour professionnels de santé",
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
    "\U0001F52C Recherche & Sciences": {  # 🔬
        "description": "Assistant pour chercheurs et scientifiques",
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
    "\U0001F4BB Développement & Code": {  # 💻
        "description": "Assistant pour développeurs et équipes tech",
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
    "\U0001F4CA Analyse & Business Intelligence": {  # 📊
        "description": "Assistant pour analystes et décideurs",
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
# (Le reste du code reste inchangé, juste remplacer tous les emojis par \Uxxxx ou \uXXXX si nécessaire)
# ===============================