"""
MicroLLM Studio - Enterprise On-Premise AI Assistant
Powered by ARSLM (en développement) + OpenAI
© 2025 Benjamin Amaad Kama - Tous droits réservés
"""

import streamlit as st
from datetime import datetime
from io import BytesIO
import base64
import json

# Import optionnels
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except:
    OPENAI_AVAILABLE = False

try:
    import PyPDF2
    PDF_AVAILABLE = True
except:
    PDF_AVAILABLE = False

try:
    import docx
    DOCX_AVAILABLE = True
except:
    DOCX_AVAILABLE = False

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="MicroLLM Studio - ARSLM Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:flywithjesus@outlook.com',
        'Report a bug': 'mailto:flywithjesus@outlook.com',
        'About': "MicroLLM Studio - Powered by ARSLM"
    }
)

# ===============================
# CUSTOM CSS
# ===============================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #667eea 100%);
        padding: 3rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        color: white;
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header .subtitle {
        font-size: 1.3rem;
        margin-top: 0.5rem;
        opacity: 0.95;
    }
    
    .arslm-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        margin-top: 1rem;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255,255,255,0.3);
    }
    
    .feature-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .feature-card:hover {
        border-color: #667eea;
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.2);
    }
    
    .feature-card h3 {
        color: #1e3c72;
        font-size: 1.5rem;
        margin-top: 0;
    }
    
    .user-msg {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 15px;
        margin: 1rem 0 1rem 20%;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .assistant-msg {
        background: #f8f9fa;
        color: #1a1a1a;
        padding: 1.2rem;
        border-radius: 15px;
        margin: 1rem 20% 1rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 6px 20px rgba(30, 60, 114, 0.3);
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0.5rem 0;
    }
    
    .info-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-left: 4px solid #667eea;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .success-box {
        background: linear-gradient(135deg, rgba(17, 153, 142, 0.1) 0%, rgba(56, 239, 125, 0.1) 100%);
        border-left: 4px solid #11998e;
        padding: 1rem;
        border-radius: 8px;
    }
    
    .warning-box {
        background: linear-gradient(135deg, rgba(255, 193, 7, 0.1) 0%, rgba(255, 152, 0, 0.1) 100%);
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 8px;
    }
    
    .analysis-result {
        background: white;
        border: 2px solid #667eea;
        border-radius: 12px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.15);
    }
    
    .analysis-result h4 {
        color: #1e3c72;
        margin-top: 0;
        font-size: 1.3rem;
    }
    
    .contact-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 15px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        margin: 2rem 0;
    }
    
    .contact-card h2 {
        margin-top: 0;
        font-size: 2.2rem;
    }
    
    .contact-input {
        background: rgba(255,255,255,0.15);
        border: 2px solid rgba(255,255,255,0.3);
        border-radius: 8px;
        padding: 0.8rem;
        color: white;
        width: 100%;
        margin: 0.5rem 0;
    }
    
    .send-button {
        background: white;
        color: #667eea;
        padding: 1rem 2.5rem;
        border-radius: 30px;
        border: none;
        font-weight: 700;
        font-size: 1.1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        width: 100%;
        margin-top: 1rem;
    }
    
    .send-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(0,0,0,0.3);
    }
    
    .download-button {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 8px;
        text-decoration: none;
        display: inline-block;
        font-weight: 600;
        transition: all 0.3s ease;
        margin: 0.5rem 0;
    }
    
    .download-button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# ===============================
# SYSTEM INFO
# ===============================
SYSTEM_INFO = {
    "platform": "MicroLLM Studio",
    "version": "2.1.0-Beta",
    "base_model": "ARSLM (en développement) + OpenAI GPT-4",
    "contact": "flywithjesus@outlook.com",
    "location": "Nguekhokh, Mbour, Sénégal",
    "author": "Benjamin Amaad Kama"
}

# ===============================
# DOMAINS
# ===============================
DOMAINS = {
    "💼 RH & Recrutement": {
        "system_prompt": "Tu es un expert RH et recrutement. Analyse les CV, aide à la rédaction de fiches de poste, évalue les candidats de manière professionnelle et confidentielle.",
        "icon": "💼",
        "color": "#667eea"
    },
    "⚖️ Juridique & Compliance": {
        "system_prompt": "Tu es un assistant juridique expert. Analyse les contrats, identifie les clauses problématiques, aide à la conformité RGPD. IMPORTANT: Rappelle toujours que tes réponses sont informatives uniquement et ne constituent pas un conseil juridique.",
        "icon": "⚖️",
        "color": "#764ba2"
    },
    "🏥 Médical & Santé": {
        "system_prompt": "Tu es un assistant médical pour professionnels de santé. Aide au diagnostic différentiel, analyse de dossiers médicaux, recherche médicale. CRUCIAL: Toujours rappeler que les informations sont pour professionnels uniquement et ne remplacent pas un avis médical. En urgence: appeler le 15.",
        "icon": "🏥",
        "color": "#11998e"
    },
    "🔬 Recherche & Sciences": {
        "system_prompt": "Tu es un assistant de recherche scientifique. Aide aux revues de littérature, analyse de données, rédaction d'articles scientifiques avec rigueur et méthode scientifique.",
        "icon": "🔬",
        "color": "#38ef7d"
    },
    "💻 Développement & Code": {
        "system_prompt": "Tu es un expert en développement logiciel. Analyse de code, détection de bugs, suggestions d'optimisation, génération de code propre et sécurisé, respect des best practices.",
        "icon": "💻",
        "color": "#667eea"
    },
    "📊 Analyse & Business Intelligence": {
        "system_prompt": "Tu es un expert data et BI. Analyse de données, génération de rapports, insights business, recommandations stratégiques basées sur les données.",
        "icon": "📊",
        "color": "#764ba2"
    }
}

# ===============================
# ANALYSIS TEMPLATES
# ===============================
ANALYSIS_TEMPLATES = {
    "📋 Résumé exécutif": """Analyse ce document et fournis un résumé exécutif structuré avec:
1. Vue d'ensemble (2-3 phrases)
2. Points clés (3-5 points principaux)
3. Recommandations ou conclusions principales

Document:
{text}""",
    
    "🔍 Analyse détaillée": """Effectue une analyse approfondie de ce document en couvrant:
1. Contexte et objectif du document
2. Structure et organisation
3. Points principaux développés
4. Arguments et preuves présentés
5. Conclusions et implications

Document:
{text}""",
    
    "📝 Points clés": """Extrais et liste les points clés de ce document sous forme de bullet points structurés par thème ou section.

Document:
{text}""",
    
    "❓ Q&A": """Génère 5-10 questions pertinentes sur ce document avec leurs réponses détaillées. Les questions doivent couvrir les aspects importants du contenu.

Document:
{text}""",
    
    "⚖️ Analyse juridique": """En tant qu'assistant juridique, analyse ce document en identifiant:
1. Type de document et parties concernées
2. Clauses principales et obligations
3. Clauses potentiellement problématiques ou à risque
4. Éléments manquants ou recommandations
5. Points d'attention particuliers

RAPPEL: Cette analyse est informative uniquement et ne constitue pas un conseil juridique.

Document:
{text}""",
    
    "🏥 Analyse médicale": """En tant qu'assistant médical, analyse ce dossier en couvrant:
1. Informations patient et contexte
2. Symptômes et signes cliniques rapportés
3. Examens et résultats
4. Diagnostic différentiel possible
5. Éléments à surveiller ou investigations complémentaires suggérées

IMPORTANT: Cette analyse est destinée aux professionnels de santé uniquement et ne remplace pas un avis médical qualifié.

Document:
{text}""",
    
    "💻 Code Review": """Effectue une revue de code professionnelle en analysant:
1. Qualité et lisibilité du code
2. Respect des bonnes pratiques et conventions
3. Bugs potentiels ou erreurs identifiées
4. Problèmes de sécurité éventuels
5. Suggestions d'optimisation et d'amélioration
6. Note globale sur 10 avec justification

Code:
{text}""",
    
    "📊 Extraction données": """Extrais et structure toutes les données pertinentes de ce document:
1. Données numériques (chiffres, statistiques, dates)
2. Informations structurées (tableaux, listes)
3. Entités nommées (personnes, organisations, lieux)
4. Présente les résultats sous forme de tableau ou liste structurée

Document:
{text}"""
}

# ===============================
# SESSION STATE
# ===============================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_domain" not in st.session_state:
    st.session_state.current_domain = "💼 RH & Recrutement"

if "page" not in st.session_state:
    st.session_state.page = "Accueil"

if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []

# ===============================
# FUNCTIONS
# ===============================
def extract_text_from_pdf(uploaded_file):
    """Extrait le texte d'un PDF avec gestion d'erreurs"""
    try:
        uploaded_file.seek(0)
        pdf_bytes = uploaded_file.read()
        pdf_file = BytesIO(pdf_bytes)
        reader = PyPDF2.PdfReader(pdf_file)
        
        if reader.is_encrypted:
            return "❌ PDF protégé par mot de passe"
        
        text = ""
        for page_num, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text()
                if page_text:
                    text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
            except:
                text += f"\n--- Page {page_num + 1} : Erreur ---\n"
        
        return text.strip() if text.strip() else "⚠️ Aucun texte extractible"
    except Exception as e:
        return f"❌ Erreur PDF: {str(e)}"

def extract_text_from_docx(uploaded_file):
    """Extrait le texte d'un DOCX"""
    try:
        uploaded_file.seek(0)
        doc = docx.Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        return text if text else "⚠️ Document vide"
    except Exception as e:
        return f"❌ Erreur DOCX: {str(e)}"

def extract_text_from_txt(uploaded_file):
    """Extrait le texte d'un TXT"""
    try:
        uploaded_file.seek(0)
        for encoding in ['utf-8', 'latin-1', 'cp1252']:
            try:
                return uploaded_file.read().decode(encoding)
            except:
                continue
        return "❌ Encodage non supporté"
    except Exception as e:
        return f"❌ Erreur TXT: {str(e)}"

def call_openai_api(messages, domain):
    """Appel à l'API OpenAI pour le chat"""
    api_key = st.secrets.get("OPENAI_API_KEY") if hasattr(st, 'secrets') else None
    
    if not api_key:
        return "❌ Clé API OpenAI manquante. Configurez-la dans les secrets Streamlit."
    
    if not OPENAI_AVAILABLE:
        return "❌ SDK OpenAI non disponible. Installez openai dans requirements.txt"
    
    try:
        client = OpenAI(api_key=api_key)
        domain_info = DOMAINS[domain]
        
        api_messages = [{"role": "system", "content": domain_info["system_prompt"]}]
        api_messages.extend(messages[-8:])
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=api_messages,
            temperature=0.3,
            max_tokens=2500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Erreur API: {str(e)}"

def analyze_document_with_gpt(text, analysis_type, custom_question=None):
    """Analyse un document avec GPT-4"""
    api_key = st.secrets.get("OPENAI_API_KEY") if hasattr(st, 'secrets') else None
    
    if not api_key:
        return "❌ Clé API OpenAI manquante. Configurez-la dans les secrets Streamlit."
    
    if not OPENAI_AVAILABLE:
        return "❌ SDK OpenAI non disponible."
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Préparer le prompt
        if custom_question:
            prompt = f"{custom_question}\n\nDocument:\n{text}"
        else:
            template = ANALYSIS_TEMPLATES.get(analysis_type, ANALYSIS_TEMPLATES["📋 Résumé exécutif"])
            prompt = template.format(text=text)
        
        # Limiter la taille du texte si trop long
        max_chars = 12000
        if len(prompt) > max_chars:
            prompt = prompt[:max_chars] + "\n\n[Document tronqué pour respecter les limites de l'API]"
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Tu es un assistant d'analyse de documents expert. Fournis des analyses précises, structurées et professionnelles."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=3000
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Erreur lors de l'analyse: {str(e)}"

def create_download_link(text, filename):
    """Crée un lien de téléchargement pour le texte"""
    b64 = base64.b64encode(text.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}" class="download-button">📥 Télécharger l\'analyse</a>'
    return href

def send_email_notification(name, email, subject, message):
    """Simule l'envoi d'un email (à connecter à un vrai service SMTP)"""
    # Dans une vraie application, utilisez smtplib ou un service comme SendGrid
    email_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "email": email,
        "subject": subject,
        "message": message
    }
    
    # Pour le moment, on sauvegarde dans l'historique
    if "contact_history" not in st.session_state:
        st.session_state.contact_history = []
    st.session_state.contact_history.append(email_data)
    
    return True

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.markdown("### 🤖 MicroLLM Studio")
    st.markdown(f"**Version {SYSTEM_INFO['version']}**")
    st.markdown("---")
    
    # Navigation
    page = st.radio(
        "Navigation",
        ["🏠 Accueil", "💬 Chat IA", "📄 Analyse Documents", "📞 Contact"],
        label_visibility="collapsed"
    )
    st.session_state.page = page
    
    st.markdown("---")
    
    # Domain selection
    if page == "💬 Chat IA":
        st.markdown("### 🎯 Domaine")
        selected_domain = st.selectbox(
            "Spécialisation",
            list(DOMAINS.keys()),
            label_visibility="collapsed"
        )
        st.session_state.current_domain = selected_domain
        
        if st.button("🗑️ Effacer historique", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    st.markdown("---")
    st.caption("© 2025 Benjamin Amaad Kama")
    st.caption(f"📍 {SYSTEM_INFO['location']}")

# ===============================
# PAGES
# ===============================

# ===== PAGE: ACCUEIL =====
if st.session_state.page == "🏠 Accueil":
    st.markdown(f"""
    <div class="main-header">
        <h1>🤖 MicroLLM Studio</h1>
        <div class="subtitle">Plateforme d'IA d'Entreprise - Sécurisée et Spécialisée</div>
        <div class="arslm-badge">
            Powered by ARSLM + OpenAI GPT-4
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## 🎯 Qu'est-ce que MicroLLM Studio ?")
        st.markdown("""
        **MicroLLM Studio** est une plateforme no-code qui permet aux entreprises de déployer 
        des assistants IA spécialisés dans des domaines sensibles : médical, juridique, RH, 
        recherche scientifique et développement.
        
        ### ✨ Caractéristiques principales
        
        - 🔒 **100% Sécurisé** : Données privées, conformité RGPD
        - 🧠 **Spécialisé** : IA adaptée à votre métier
        - 📚 **Multi-formats** : PDF, Word, Code, Texte
        - 🎯 **No-Code** : Interface simple et intuitive
        - 🌍 **Multilingue** : Français, Anglais, etc.
        - ⚡ **Rapide** : Réponses en quelques secondes
        """)
        
        features = [
            {"icon": "💬", "title": "Chat IA Spécialisé", "desc": "Conversez avec un assistant expert dans votre domaine"},
            {"icon": "📄", "title": "Analyse de Documents", "desc": "Analysez PDF, Word, Code avec GPT-4"},
            {"icon": "🔍", "title": "8 Types d'Analyses", "desc": "Résumé, juridique, médical, code review..."},
            {"icon": "📊", "title": "Export des Résultats", "desc": "Téléchargez vos analyses au format texte"}
        ]
        
        for feat in features:
            st.markdown(f"""
            <div class="feature-card">
                <h3>{feat['icon']} {feat['title']}</h3>
                <p>{feat['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 Statistiques")
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Domaines</div>
            <div class="metric-value">{len(DOMAINS)}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-l