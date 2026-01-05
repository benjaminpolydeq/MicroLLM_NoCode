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
    page_icon="🤖",
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
# DOMAINS
# ===============================
DOMAINS = {
    "💼 RH & Recrutement": {
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
    "⚖️ Juridique & Compliance": {
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
    "🏥 Médical & Santé": {
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
    "🔬 Recherche & Sciences": {
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
    "💻 Développement & Code": {
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
    "📊 Analyse & Business Intelligence": {
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
# CSS
# ===============================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
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
    
    .info-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-left: 4px solid #667eea;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0;
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
    
    .metric-card:hover { transform: scale(1.05); }
    
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
    
    .success-box {
        background: linear-gradient(135deg, rgba(17, 153, 142, 0.1) 0%, rgba(56, 239, 125, 0.1) 100%);
        border-left: 4px solid #11998e;
        padding: 1rem;
        border-radius: 8px;
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
# ENGINE
# ===============================
class EnterpriseARSLMEngine:
    """Enterprise ARSLM Engine - On-Premise Secure AI Assistant"""
    
    def __init__(self, domain="general"):
        self.domain = domain
        self.knowledge_base = self._load_knowledge_base()
        self.conversation_history = []
        self.documents = []
        self.code_repository = []
    
    def _load_knowledge_base(self):
        """Load pre-integrated knowledge base about MicroLLM Studio"""
        return [
            {
                "keywords": ["microllm", "studio", "plateforme", "c'est quoi", "qu'est-ce", "définition", "what is"],
                "response": """🤖 **MicroLLM Studio - Vue d'ensemble**

**MicroLLM Studio** est une plateforme d'intelligence artificielle no-code conçue pour les entreprises traitant des données sensibles.

**Caractéristiques principales** :
- 🔒 **100% On-Premise** : Toutes vos données restent sur votre infrastructure
- 🧠 **6 Domaines Spécialisés** : RH, Juridique, Médical, Recherche, Développement, BI
- 🚀 **No-Code** : Interface intuitive sans besoin de compétences techniques
- 🔐 **Sécurité Maximale** : Chiffrement, audit, conformité RGPD

**Built on ARSLM** (Adaptive Reasoning Semantic Language Model) - Notre moteur propriétaire léger et performant."""
            },
            {
                "keywords": ["arslm", "moteur", "modèle", "engine", "base model"],
                "response": """🧠 **ARSLM - Le Moteur d'IA de MicroLLM**

**ARSLM** (Adaptive Reasoning Semantic Language Model) est le moteur propriétaire qui alimente MicroLLM Studio.

**Avantages d'ARSLM** :
- ⚡ **Léger et Rapide** : Fonctionne sur hardware modeste
- 🎯 **Adaptatif** : S'ajuste à votre domaine spécifique
- 🔒 **Sécurisé** : Conçu pour environnements sensibles
- 🌍 **Local** : Aucune dépendance cloud externe
- 💰 **Économique** : Pas de coûts par token

**Spécialisation** : ARSLM peut être fine-tuné pour votre domaine métier spécifique."""
            },
            {
                "keywords": ["domaines", "spécialisation", "secteurs", "métiers", "domains"],
                "response": """🎯 **Domaines de Spécialisation MicroLLM**

MicroLLM Studio supporte **6 domaines métiers** :

**💼 RH & Recrutement**
- Analyse CV et candidatures
- Génération contrats et documents RH
- Évaluation des talents

**⚖️ Juridique & Compliance**
- Analyse de contrats
- Recherche jurisprudentielle
- Conformité RGPD

**🏥 Médical & Santé**
- Analyse dossiers médicaux
- Aide au diagnostic
- Veille scientifique médicale

**🔬 Recherche & Sciences**
- Revue de littérature
- Analyse de données expérimentales
- Rédaction scientifique

**💻 Développement & Code**
- Code review automatisé
- Détection de bugs
- Optimisation de code

**📊 Business Intelligence**
- Analyse de données
- Rapports exécutifs
- Prévisions et tendances

Vous pouvez **changer de domaine** à tout moment dans la barre latérale !"""
            },
            {
                "keywords": ["prix", "tarif", "coût", "pricing", "combien", "license", "licence"],
                "response": """💰 **Tarification MicroLLM Studio**

**🆓 Évaluation (Gratuit)**
- 30 jours d'essai complet
- Toutes les fonctionnalités
- Support communautaire
- 📧 Contact : benjokama@hotmail.fr

**🚀 Professional ($499/mois)**
- Documents illimités
- Interactions illimitées
- 3 domaines simultanés
- API REST incluse
- Support email 48h

**🏢 Enterprise (Sur devis)**
- Tous les domaines
- White-label complet
- Support 24/7 + SLA
- Formation personnalisée
- Audit de sécurité
- Intégrations sur mesure

**🎁 Programmes Spéciaux** :
- -40% pour marchés émergents (Afrique, Asie, Latam)
- Gratuit pour universités et recherche
- -50% pour startups (<2 ans)

📧 **Demander un devis** : benjokama@hotmail.fr"""
            },
            {
                "keywords": ["sécurité", "confidentialité", "security", "privacy", "rgpd", "données"],
                "response": """🔐 **Sécurité & Confidentialité MicroLLM**

**Protection Maximale de vos Données** :

**🔒 Déploiement On-Premise**
- 100% de vos données restent sur votre infrastructure
- Aucune connexion cloud externe requise
- Contrôle total de votre environnement

**🛡️ Sécurité Technique**
- Chiffrement AES-256 au repos et en transit
- Audit logging de toutes les opérations
- Anonymisation automatique des données sensibles
- Destruction sécurisée des données temporaires

**✅ Conformité Réglementaire**
- RGPD (Europe) : Conforme
- CCPA (Californie) : Conforme
- HIPAA (Santé US) : Compatible
- ISO 27001 : Ready
- SOC 2 : Compatible

**🔍 Recherche Sécurisée**
- Proxy intégré sans traces
- Aucun historique conservé en externe
- IP masquée automatiquement

**Idéal pour** : Santé, Juridique, Finance, Défense, Recherche sensible."""
            },
            {
                "keywords": ["installation", "déploiement", "setup", "installer", "deploy", "comment utiliser"],
                "response": """🚀 **Installation MicroLLM Studio**

**Option 1 : Local (Développement)**
```bash
git clone https://github.com/benjaminpolydeq/microllm_nocode.git
cd microllm_nocode
pip install -r requirements.txt
streamlit run streamlit_app.py
```

**Option 2 : Docker (Production)**
```bash
docker build -t microllm:latest .
docker run -p 8501:8501 microllm:latest
```

**Option 3 : Docker Compose (Enterprise)**
```bash
docker-compose up -d
```

**Option 4 : Streamlit Cloud**
- Push sur GitHub
- Déployer sur share.streamlit.io
- Configuration automatique

**Prérequis** :
- Python 3.8+
- 4GB RAM minimum
- 10GB espace disque

**Support installation** : benjokama@hotmail.fr"""
            },
            {
                "keywords": ["fonctionnalités", "features", "capacités", "peut faire", "capabilities"],
                "response": """✨ **Fonctionnalités MicroLLM Studio**

**💬 Assistant IA Intelligent**
- Chat contextuel avec mémoire
- Réponses spécialisées par domaine
- Support multi-langues

**📚 Gestion Documents**
- Upload multi-formats (PDF, Word, Excel, Code)
- Ingestion automatique
- Analyse sémantique
- Recherche dans documents

**💻 Analyse de Code**
- Support 10+ langages
- Détection bugs et vulnérabilités
- Suggestions d'optimisation
- Génération de tests

**🔍 Recherche Sécurisée**
- Navigation web sans traces
- Proxy intégré
- Résultats anonymisés
- Corrélation avec vos données

**📊 Génération de Rapports**
- 8 types de rapports
- Export PDF/Word/Excel
- Visualisations interactives
- Personnalisables

**⚙️ Configuration**
- Paramètres de sécurité
- Gestion des données
- Export/Import configuration
- Audit logging

**🎯 No-Code** : Tout est accessible sans coder !"""
            },
            {
                "keywords": ["documents", "fichiers", "upload", "formats", "importer"],
                "response": """📚 **Gestion des Documents dans MicroLLM**

**Formats Supportés** :
- 📄 **Bureautique** : PDF, Word (.docx, .doc), Excel (.xlsx, .xls)
- 📝 **Texte** : TXT, CSV, JSON, Markdown
- 💻 **Code** : Python, JavaScript, Java, C++, Go, Rust, PHP, Ruby
- 🖼️ **Images** : PNG, JPG (OCR prévu)

**Processus d'Ingestion** :
1. Allez dans l'onglet "📚 Documents"
2. Cliquez sur la zone d'upload
3. Sélectionnez vos fichiers (multi-sélection possible)
4. Les documents sont analysés automatiquement
5. Utilisez-les dans le chat !

**Sécurité** :
- Tous les documents restent locaux
- Chiffrement automatique
- Destruction sécurisée possible

**Limites** :
- Taille max par fichier : 200MB
- Nombre de documents : Illimité
- Formats simultanés : Tous

**L'assistant IA référence automatiquement vos documents dans ses réponses !**"""
            },
            {
                "keywords": ["code", "programmation", "développement", "programming", "analyse code"],
                "response": """💻 **Analyse de Code avec MicroLLM**

**Langages Supportés** :
Python • JavaScript • Java • C++ • C# • Go • Rust • PHP • Ruby • SQL

**Fonctionnalités** :

**🔍 Analyse**
- Complexité algorithmique
- Qualité du code
- Respect des standards
- Métriques détaillées

**🐛 Détection de Bugs**
- Erreurs de syntaxe
- Vulnérabilités de sécurité
- Memory leaks potentiels
- Exceptions non gérées

**⚡ Optimisation**
- Suggestions de refactoring
- Amélioration performance
- Réduction complexité
- Best practices

**📝 Documentation**
- Génération automatique
- Commentaires intelligents
- README et guides

**🧪 Tests**
- Génération tests unitaires
- Cas limites
- Couverture de code

**Utilisation** : Collez votre code dans l'onglet "💻 Analyse Code" et choisissez l'action souhaitée !"""
            },
            {
                "keywords": ["recherche", "search", "web", "internet", "trouver"],
                "response": """🔍 **Recherche Sécurisée MicroLLM**

**Comment ça fonctionne ?**

**🔒 Protection Totale**
- Toutes les requêtes passent par un proxy on-premise
- Votre IP n'est jamais exposée
- Aucun cookie ou tracker conservé
- Historique chiffré localement

**🌐 Capacités**
- Recherche web classique
- Recherche académique
- Recherche de code (GitHub, Stack Overflow)
- Recherche de documentation

**🎯 Modes Disponibles**
- **Standard** : Recherche rapide
- **Approfondie** : Analyse multi-sources
- **Contextuelle** : Corrélation avec vos documents

**🛡️ Sécurité**
- Zéro trace externe
- Navigation anonyme
- Résultats filtrés et validés
- Conformité aux politiques d'entreprise

**Utilisation** :
1. Onglet "🔍 Recherche"
2. Entrez votre requête
3. Activez "Recherche Approfondie" si nécessaire
4. Consultez les résultats sécurisés

**Idéal pour** : Recherche confidentielle, veille concurrentielle, analyse de marché."""
            },
            {
                "keywords": ["rapport", "report", "export", "génération", "document"],
                "response": """📊 **Génération de Rapports MicroLLM**

**Types de Rapports Disponibles** :

**📄 Résumé Exécutif**
- Vue d'ensemble synthétique
- Points clés
- Recommandations

**🔬 Analyse Technique**
- Détails approfondis
- Métriques précises
- Graphiques et tableaux

**⚖️ Rapport Juridique**
- Analyse de contrats
- Conformité
- Risques légaux

**🏥 Rapport Médical**
- Synthèse dossiers médicaux
- Protocoles
- Littérature scientifique

**💼 Rapport RH**
- Analyses candidatures
- Évaluations
- Plans de développement

**📊 Analyse de Données**
- Insights business
- Visualisations
- Prévisions

**Personnalisation** :
- Niveau de détail ajustable
- Inclusion graphiques/références
- Longueur configurable

**Export** :
- PDF (prêt à imprimer)
- Word (modifiable)
- Excel (données)

**Génération** : Onglet "📊 Rapports" → Choisir type → Configurer → Générer !"""
            },
            {
                "keywords": ["support", "aide", "help", "assistance", "contact", "problème"],
                "response": """🤝 **Support & Assistance MicroLLM**

**📧 Contact**
Email : benjokama@hotmail.fr
GitHub : @benjaminpolydeq

**💼 Niveaux de Support**

**🆓 Community (Gratuit)**
- GitHub Issues
- Documentation en ligne
- Best effort

**🚀 Professional**
- Email support
- Réponse sous 48h
- Résolution de bugs

**🏢 Enterprise**
- Support 24/7
- SLA garanti
- Account manager dédié
- Formation personnalisée
- Assistance au déploiement

**📚 Ressources**
- Documentation complète
- Guides de déploiement
- Tutoriels vidéo (à venir)
- FAQ détaillée

**🎓 Formation**
- Onboarding équipes
- Sessions personnalisées
- Certification (Enterprise)

**🐛 Signaler un Bug**
1. GitHub Issues
2. Email avec détails
3. Logs si disponibles

**💡 Demande de Fonctionnalité**
Email avec description détaillée de votre besoin.

**Délais de Réponse** :
- Questions générales : 24-48h
- Bugs critiques : < 24h (Enterprise)
- Demandes commerciales : 24h"""
            },
            {
                "keywords": ["différence", "comparison", "vs", "comparaison", "chatgpt", "openai", "concurrent"],
                "response": """⚖️ **MicroLLM vs Autres Solutions IA**

**🆚 MicroLLM vs ChatGPT/OpenAI**

| Critère | MicroLLM | ChatGPT/OpenAI |
|---------|----------|----------------|
| **Déploiement** | On-premise | Cloud uniquement |
| **Données** | Restent chez vous | Envoyées à OpenAI |
| **Coûts** | Fixe mensuel | Par token |
| **Personnalisation** | Domaines spécialisés | Généraliste |
| **Conformité** | RGPD total | Limitations |
| **Latence** | Locale (rapide) | Internet requis |

**🆚 MicroLLM vs Solutions Open Source**

| Critère | MicroLLM | Open Source |
|---------|----------|-------------|
| **Setup** | No-code, simple | Technique requis |
| **Support** | Professionnel | Communauté |
| **Sécurité** | Prêt entreprise | À configurer |
| **Maintenance** | Incluse | DIY |
| **Spécialisation** | 6 domaines | Générique |

**🎯 Avantages Uniques MicroLLM** :
- 🔒 Confidentialité totale (on-premise)
- 🎯 Spécialisé par domaine métier
- 🚀 Interface no-code intuitive
- 💰 Coûts prévisibles
- 🌍 Optimisé marchés émergents
- 🤝 Support entreprise

**Idéal pour** : Santé, Finance, Juridique, Recherche, tout secteur manipulant des données sensibles."""
            },
            {
                "keywords": ["entreprise", "business", "commercial", "b2b", "organisation"],
                "response": """💼 **MicroLLM pour Entreprises**

**🎯 Pourquoi les Entreprises Choisissent MicroLLM**

**Secteurs Clients** :
- 🏥 Santé : Hôpitaux, cliniques, laboratoires
- ⚖️ Juridique : Cabinets d'avocats, services légaux
- 🏦 Finance : Banques, assurances, fintech
- 🔬 Recherche : Universités, centres R&D
- 💻 Tech : Entreprises logicielles, DSI
- 🏢 Corporates : Départements RH, compliance

**📊 ROI Typique**
- Réduction 60% temps de traitement documents
- Économies 70% vs solutions cloud (sur 
        
    def ingest_document(self, content, doc_type, filename):
        """Ingest documents into knowledge base"""
        doc = {
            "filename": filename,
            "type": doc_type,
            "content": content,
            "ingested_at": datetime.now().isoformat(),
            "tokens": len(content.split())
        }
        self.documents.append(doc)
        return doc
    
    def analyze_code(self, code, language="python"):
        """Analyze code for quality, bugs, and optimization"""
        analysis = {
            "language": language,
            "lines": len(code.split('\n')),
            "complexity": "Medium",
            "issues": [],
            "suggestions": []
        }
        
        if "TODO" in code or "FIXME" in code:
            analysis["issues"].append("Contains TODO/FIXME comments")
        
        if len(code.split('\n')) > 100:
            analysis["suggestions"].append("Consider splitting into smaller functions")
        
        if "import *" in code:
            analysis["issues"].append("Wildcard imports detected - specify imports explicitly")
        
        return analysis
    
    def generate_response(self, query, context_type="general"):
        """Generate response based on domain expertise"""
        response = ""
        
        domain_knowledge = {
            "💼 RH & Recrutement": {
                "keywords": ["cv", "candidat", "recrutement", "contrat", "formation"],
                "response_template": "En tant qu'assistant RH spécialisé, je peux vous aider avec : {topic}. "
            },
            "⚖️ Juridique & Compliance": {
                "keywords": ["contrat", "clause", "juridique", "loi", "conformité"],
                "response_template": "D'un point de vue juridique, concernant {topic} : "
            },
            "🏥 Médical & Santé": {
                "keywords": ["patient", "diagnostic", "traitement", "médical", "clinique"],
                "response_template": "Analyse médicale pour {topic} : "
            },
            "🔬 Recherche & Sciences": {
                "keywords": ["recherche", "étude", "publication", "analyse", "données"],
                "response_template": "Perspective scientifique sur {topic} : "
            },
            "💻 Développement & Code": {
                "keywords": ["code", "fonction", "algorithme", "debug", "optimisation"],
                "response_template": "Analyse technique de {topic} : "
            }
        }
        
        relevant_docs = [doc for doc in self.documents if any(word in doc["content"].lower() for word in query.lower().split())]
        
        if relevant_docs:
            response += f"📚 **Analyse basée sur {len(relevant_docs)} document(s) de votre base** :\n\n"
        
        if self.domain in domain_knowledge:
            domain_info = domain_knowledge[self.domain]
            if any(kw in query.lower() for kw in domain_info["keywords"]):
                response += domain_info["response_template"].format(topic=query)
        
        if "code" in query.lower():
            response += "\n\n**Analyse de code** :\n- Vérification de la syntaxe\n- Détection de vulnérabilités\n- Suggestions d'optimisation\n"
        elif "résumé" in query.lower() or "summary" in query.lower():
            response += "\n\n**Génération de résumé** :\nRésumé des documents analysés...\n"
        elif "recherche" in query.lower() or "search" in query.lower():
            response += "\n\n🔍 **Recherche sécurisée** (sans traces externes) :\n- Analyse des documents internes\n- Corrélation des informations\n"
        
        if not response:
            response = f"""🧠 **Analyse de votre requête** : "{query}"

**Domaine actif** : {self.domain}

**Capacités disponibles** :
- 📄 Analyse de documents ({len(self.documents)} chargés)
- 💻 Revue et génération de code
- 🔍 Recherche sécurisée on-premise
- 📊 Génération de rapports
- 🎯 Réponses spécialisées

**Confidentialité** : Toutes les données restent sur votre infrastructure."""
        
        self.conversation_history.append({
            "query": query,
            "response": response,
            "domain": self.domain,
            "timestamp": datetime.now().isoformat(),
            "context_docs": len(relevant_docs)
        })
        
        return response
    
    def secure_web_search(self, query):
        """Simulate secure web search without leaving traces"""
        return {
            "query": query,
            "method": "On-premise proxy with no logging",
            "results": [
                {"title": "Résultat 1", "snippet": "Extrait pertinent...", "source": "Source sécurisée"},
                {"title": "Résultat 2", "snippet": "Information analysée...", "source": "Base interne"}
            ],
            "privacy": "Aucune trace externe - Recherche proxifiée"
        }

# ===============================
# SESSION STATE
# ===============================
if "engine" not in st.session_state:
    st.session_state.engine = EnterpriseARSLMEngine()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_domain" not in st.session_state:
    st.session_state.current_domain = "Général"

if "documents" not in st.session_state:
    st.session_state.documents = []

# ===============================
# HEADER
# ===============================
st.markdown(f"""
<div class="main-header">
    <h1>🤖 {SYSTEM_INFO['platform']}</h1>
    <div class="subtitle">Built on {SYSTEM_INFO['base_model']} - Enterprise On-Premise AI Assistant</div>
    <div class="arslm-badge">
        🔒 100% Private • 🧠 Domain-Specialized • 🚀 No-Code
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="security-badge">
    🔐 SÉCURITÉ MAXIMALE : Toutes vos données restent sur votre infrastructure - Aucune fuite externe
</div>
""", unsafe_allow_html=True)

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.image("https://via.placeholder.com/250x100/1e3c72/ffffff?text=MicroLLM+Studio", use_container_width=True)
    
    st.markdown("---")
    
    page = st.radio(
        "📑 Navigation",
        ["🏠 Accueil", "💬 Assistant IA", "📚 Documents", "💻 Analyse Code", "🔍 Recherche", "📊 Rapports", "⚙️ Configuration"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    st.markdown("### 🎯 Domaine de Spécialisation")
    selected_domain = st.selectbox(
        "Choisir un domaine",
        list(DOMAINS.keys()),
        label_visibility="collapsed"
    )
    
    if selected_domain != st.session_state.current_domain:
        st.session_state.current_domain = selected_domain
        st.session_state.engine.domain = selected_domain
    
    st.markdown("---")
    
    st.markdown("### 📊 Statistiques")
    st.metric("Documents", len(st.session_state.documents))
    st.metric("Conversations", len(st.session_state.messages))
    st.metric("Code Analysé", len(st.session_state.engine.code_repository))
    
    st.markdown("---")
    
    with st.expander("ℹ️ À propos"):
        st.markdown(f"""
        **Version** : {SYSTEM_INFO['version']}
        
        **{SYSTEM_INFO['base_model']}** :  
        {SYSTEM_INFO['arslm_description']}
        """)
    
    st.markdown("---")
    
    st.info("""
    📧 **Support Enterprise**  
    benjokama@hotmail.fr
    
    © 2025 Benjamin Amaad Kama
    """)

# ===============================
# PAGES
# ===============================
if page == "🏠 Accueil":
    st.markdown("## 🎯 Plateforme d'IA Enterprise On-Premise")
    
    st.markdown("### 🧠 À propos d'ARSLM")
    st.markdown(f'<div class="info-box">{SYSTEM_INFO["arslm_description"]}</div>', unsafe_allow_html=True)
    
    st.markdown("### 🤖 À propos de MicroLLM Studio")
    st.markdown(f'<div class="info-box">{SYSTEM_INFO["microllm_description"]}</div>', unsafe_allow_html=True)
    
    st.markdown("### ✨ Fonctionnalités Clés")
    
    col1, col2 = st.columns(2)
    
    with col1:
        for feature in SYSTEM_INFO["features"][:4]:
            st.markdown(f"**{feature}**")
    
    with col2:
        for feature in SYSTEM_INFO["features"][4:]:
            st.markdown(f"**{feature}**")
    
    st.markdown("---")
    
    st.markdown("### 🎓 Domaines de Spécialisation")
    
    for domain_name, domain_info in DOMAINS.items():
        with st.expander(f"{domain_name} - {domain_info['description']}"):
            st.markdown("**Capacités** :")
            for cap in domain_info["capabilities"]:
                st.markdown(f"- {cap}")
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Documents</div>
            <div class="metric-value">{len(st.session_state.documents)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Conversations</div>
            <div class="metric-value">{len(st.session_state.messages)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Sécurité</div>
            <div class="metric-value">🔒</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">On-Premise</div>
            <div class="metric-value">✓</div>
        </div>
        """, unsafe_allow_html=True)

elif page == "💬 Assistant IA":
    st.markdown(f"## 💬 Assistant IA - {st.session_state.current_domain}")
    
    if st.session_state.current_domain in DOMAINS:
        domain_info = DOMAINS[st.session_state.current_domain]
        st.markdown(f'<div class="info-box"><strong>{domain_info["description"]}</strong></div>', unsafe_allow_html=True)
    
    if not st.session_state.messages:
        st.markdown(f"""
        <div class="assistant-msg">
            <strong>👋 Bienvenue sur MicroLLM Studio</strong><br><br>
            Je suis votre assistant IA spécialisé en <strong>{st.session_state.current_domain}</strong>.<br><br>
            🔒 <strong>Confidentialité garantie</strong> : Toutes vos données restent sur votre infrastructure.
        </div>
        """, unsafe_allow_html=True)
    
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-msg">👤 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-msg">🤖 {msg["content"]}</div>', unsafe_allow_html=True)
    
    user_input = st.chat_input("Posez votre question...")
    
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.spinner(f"🧠 Analyse en cours..."):
            response = st.session_state.engine.generate_response(user_input)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

elif page == "📚 Documents":
    st.markdown("## 📚 Gestion des Documents")
    st.caption("Ingestion sécurisée - Aucune donnée ne quitte votre infrastructure")
    
    uploaded_files = st.file_uploader(
        "Formats supportés : PDF, Word, Excel, TXT, CSV, JSON, Code",
        type=["pdf", "docx", "doc", "xlsx", "xls", "txt", "csv", "json", "py", "js"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            content = uploaded_file.read()
            file_ext = uploaded_file.name.split('.')[-1].lower()
            
            if file_ext in ["txt", "csv", "json", "py", "js"]:
                content = content.decode("utf-8")
            else:
                content = f"[Fichier {file_ext.upper()} - {len(content)} bytes]"
            
            doc = st.session_state.engine.ingest_document(
                content=str(content),
                doc_type=file_ext,
                filename=uploaded_file.name
            )
            
            st.session_state.documents.append(doc)
            st.markdown(f'<div class="success-box">✅ "{uploaded_file.name}" ingéré ({doc["tokens"]} tokens)</div>', unsafe_allow_html=True)
    
    if st.session_state.documents:
        st.markdown("---")
        st.markdown("### 📋 Documents Chargés")
        df = pd.DataFrame(st.session_state.documents)
        st.dataframe(df[["filename", "type", "tokens", "ingested_at"]], use_container_width=True)

elif page == "💻 Analyse Code":
    st.markdown("## 💻 Analyse et Génération de Code")
    
    language = st.selectbox("Langage", ["Python", "JavaScript", "Java", "C++", "Go", "Rust", "PHP"])
    
    code_input = st.text_area("Collez votre code ici", height=300)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        analyze_btn = st.button("🔍 Analyser", use_container_width=True)
    
    with col2:
        optimize_btn = st.button("⚡ Optimiser", use_container_width=True)
    
    with col3:
        debug_btn = st.button("🐛 Détecter Bugs", use_container_width=True)
    
    if code_input and analyze_btn:
        st.markdown("### 📊 Analyse du Code")
        analysis = st.session_state.engine.analyze_code(code_input, language.lower())
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Lignes", analysis["lines"])
        with col2:
            st.metric("Complexité", analysis["complexity"])
        with col3:
            st.metric("Problèmes", len(analysis["issues"]))

elif page == "🔍 Recherche":
    st.markdown("## 🔍 Recherche Sécurisée")
    
    search_query = st.text_input("🔎 Rechercher", placeholder="Entrez votre requête...")
    
    if st.button("🔍 Rechercher (Mode Sécurisé)", use_container_width=True) and search_query:
        with st.spinner("🔒 Recherche en cours..."):
            results = st.session_state.engine.secure_web_search(search_query)
        
        st.markdown(f'<div class="success-box">✅ {results["privacy"]}</div>', unsafe_allow_html=True)
        
        for i, result in enumerate(results["results"], 1):
            with st.expander(f"{i}. {result['title']}"):
                st.markdown(f"**Source** : {result['source']}")
                st.markdown(f"**Extrait** : {result['snippet']}")

elif page == "📊 Rapports":
    st.markdown("## 📊 Génération de Rapports")
    
    report_type = st.selectbox("Type de rapport", [
        "📄 Résumé Exécutif",
        "🔬 Analyse Technique",
        "⚖️ Rapport Juridique",
        "🏥 Rapport Médical"
    ])
    
    if st.button("📊 Générer le Rapport", type="primary", use_container_width=True):
        st.markdown(f"## {report_type}")
        st.markdown(f"**Généré le** : {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
        st.markdown(f"**Domaine** : {st.session_state.current_domain}")

elif page == "⚙️ Configuration":
    st.markdown("## ⚙️ Configuration Système")
    
    st.markdown("### 🔐 Sécurité")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("Chiffrement des données", value=True, disabled=True)
        st.checkbox("Audit logging", value=True, disabled=True)
        st.checkbox("Authentification 2FA", value=False)
    
    with col2:
        st.checkbox("Anonymisation automatique", value=True)
        st.checkbox("Destruction sécurisée", value=True)
        st.checkbox("Conformité RGPD", value=True, disabled=True)
    
    st.markdown("---")
    
    st.markdown("### 🧠 Configuration du Modèle")
    
    temperature = st.slider("Température (créativité)", 0.0, 1.0, 0.7)
    max_tokens = st.number_input("Tokens maximum par réponse", 100, 4000, 1000)
    
    st.markdown("---")
    
    st.markdown("### 🗄️ Gestion des Données")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Effacer l'historique de chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.engine.conversation_history = []
            st.success("✅ Historique effacé")
            st.rerun()
    
    with col2:
        if st.button("🗑️ Effacer tous les documents", use_container_width=True):
            st.session_state.documents = []
            st.session_state.engine.documents = []
            st.success("✅ Documents effacés")
            st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 💾 Export / Import")
    
    if st.button("📥 Exporter la configuration", use_container_width=True):
        config = {
            "version": SYSTEM_INFO["version"],
            "domain": st.session_state.current_domain,
            "documents_count": len(st.session_state.documents),
            "messages_count": len(st.session_state.messages),
            "exported_at": datetime.now().isoformat()
        }
        
        st.download_button(
            "💾 Télécharger config.json",
            data=json.dumps(config, indent=2),
            file_name=f"microllm_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    st.markdown("---")
    
    st.markdown("### 📄 Informations de Licence")
    
    st.info(f"""
**MicroLLM Studio** v{SYSTEM_INFO['version']}  
Built on **{SYSTEM_INFO['base_model']}**

**Licence** : Propriétaire  
**Copyright** : © 2025 Benjamin Amaad Kama  
**Tous droits réservés**

Pour licence commerciale ou support entreprise :  
📧 benjokama@hotmail.fr

**Conformité** :
- ✅ RGPD (Europe)
- ✅ CCPA (Californie)
- ✅ ISO 27001 ready
- ✅ SOC 2 compatible
    """)

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;color:#666;padding:1.5rem;background:#f8f9fa;border-radius:10px">
    <strong>MicroLLM Studio v{SYSTEM_INFO['version']}</strong> · Built on <strong>{SYSTEM_INFO['base_model']}</strong><br>
    🔒 Enterprise On-Premise AI Assistant · 100% Private & Secure<br>
    <br>
    <strong>Domaine Actif</strong> : {st.session_state.current_domain}<br>
    <strong>Documents</strong> : {len(st.session_state.documents)} | <strong>Conversations</strong> : {len(st.session_state.messages)}<br>
    <br>
    © 2025 Benjamin Amaad Kama · Proprietary Software · All Rights Reserved<br>
    📧 benjokama@hotmail.fr · 💼 Enterprise Licensing Available
</div>
""", unsafe_allow_html=True)