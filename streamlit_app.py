"""
MicroLLM Studio - Enterprise On-Premise AI Assistant
Powered by ARSLM (en développement) + OpenAI
© 2025 Benjamin Amaad Kama - Tous droits réservés
"""

import streamlit as st
from datetime import datetime
from io import BytesIO
import base64

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
    
    .arslm-announce {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.3);
    }
    
    .arslm-announce h2 {
        margin: 0 0 1rem 0;
        font-size: 2rem;
    }
    
    .collab-button {
        background: white;
        color: #667eea;
        padding: 1rem 2rem;
        border-radius: 30px;
        text-decoration: none;
        display: inline-block;
        font-weight: 700;
        margin-top: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .collab-button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 25px rgba(0,0,0,0.3);
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
</style>
""", unsafe_allow_html=True)

# ===============================
# SYSTEM INFO
# ===============================
SYSTEM_INFO = {
    "platform": "MicroLLM Studio",
    "version": "2.0.0-Beta",
    "base_model": "ARSLM (en développement) + OpenAI",
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
# SESSION STATE
# ===============================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_domain" not in st.session_state:
    st.session_state.current_domain = "💼 RH & Recrutement"

if "page" not in st.session_state:
    st.session_state.page = "Accueil"

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
    """Appel à l'API OpenAI"""
    api_key = st.secrets.get("OPENAI_API_KEY") if hasattr(st, 'secrets') else None
    
    if not api_key:
        return "❌ Clé API OpenAI manquante. Configurez-la dans les secrets Streamlit."
    
    if not OPENAI_AVAILABLE:
        return "❌ SDK OpenAI non disponible. Installez openai dans requirements.txt"
    
    try:
        client = OpenAI(api_key=api_key)
        domain_info = DOMAINS[domain]
        
        api_messages = [{"role": "system", "content": domain_info["system_prompt"]}]
        api_messages.extend(messages[-8:])  # 8 derniers messages
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=api_messages,
            temperature=0.3,
            max_tokens=2500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Erreur API: {str(e)}"

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
        ["🏠 Accueil", "💬 Chat IA", "📄 Traitement Documents", "🔧 À propos ARSLM", "📞 Contact"],
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
    # Header
    st.markdown(f"""
    <div class="main-header">
        <h1>🤖 MicroLLM Studio</h1>
        <div class="subtitle">Plateforme d'IA d'Entreprise - Sécurisée et Spécialisée</div>
        <div class="arslm-badge">
            Powered by ARSLM (en développement) + OpenAI
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Présentation
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
        
        st.markdown("### 🚀 Fonctionnalités actuelles")
        
        features = [
            {
                "icon": "💬",
                "title": "Chat IA Spécialisé",
                "desc": "Conversez avec un assistant expert dans votre domaine"
            },
            {
                "icon": "📄",
                "title": "Traitement de Documents",
                "desc": "Analysez PDF, Word, Code avec extraction intelligente"
            },
            {
                "icon": "🔍",
                "title": "Analyse Contextuelle",
                "desc": "Compréhension sémantique de vos documents"
            },
            {
                "icon": "📊",
                "title": "Rapports Automatisés",
                "desc": "Génération de résumés et analyses détaillées"
            }
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
            <div class="metric-label">Messages</div>
            <div class="metric-value">{len(st.session_state.messages)}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🎯 Domaines disponibles")
        for domain_name, domain_info in DOMAINS.items():
            st.markdown(f"{domain_info['icon']} {domain_name}")

# ===== PAGE: CHAT IA =====
elif st.session_state.page == "💬 Chat IA":
    st.markdown(f"### 💬 Assistant IA - {st.session_state.current_domain}")
    
    domain_info = DOMAINS[st.session_state.current_domain]
    
    st.markdown(f"""
    <div class="info-box">
        <strong>{domain_info['icon']} Domaine actif :</strong> {st.session_state.current_domain}<br>
        <strong>Mode :</strong> Chat conversationnel avec contexte
    </div>
    """, unsafe_allow_html=True)
    
    # Afficher l'historique
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="user-msg">
                <strong>👤 Vous:</strong><br>{msg['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="assistant-msg">
                <strong>🤖 Assistant {st.session_state.current_domain}:</strong><br>
                {msg['content']}
            </div>
            """, unsafe_allow_html=True)
    
    # Input
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Votre message",
            placeholder=f"Posez une question liée au domaine {st.session_state.current_domain}...",
            height=120
        )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            submitted = st.form_submit_button("📤 Envoyer", type="primary", use_container_width=True)
        with col2:
            examples = st.form_submit_button("💡 Exemples", use_container_width=True)
        
        if submitted and user_input.strip():
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            with st.spinner("🤖 Génération..."):
                response = call_openai_api(st.session_state.messages, st.session_state.current_domain)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        
        if examples:
            st.info("💡 Exemples de questions selon le domaine actif")

# ===== PAGE: TRAITEMENT DOCUMENTS =====
elif st.session_state.page == "📄 Traitement Documents":
    st.markdown("### 📄 Traitement Intelligent de Documents")
    
    st.markdown("""
    <div class="info-box">
        <h4>📚 Formats supportés</h4>
        <ul>
            <li>📕 PDF - Documents Adobe (texte extractible)</li>
            <li>📘 DOCX - Microsoft Word</li>
            <li>📄 TXT - Fichiers texte brut</li>
            <li>💻 Code - Python, JavaScript, Java, etc.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "📁 Choisir un fichier",
        type=["pdf", "docx", "txt", "py", "js", "java", "cpp", "md"],
        help="Glissez-déposez ou cliquez"
    )
    
    if uploaded_file:
        file_size = uploaded_file.size / 1024 / 1024
        st.success(f"✅ **{uploaded_file.name}** ({file_size:.2f} MB)")
        
        if st.button("🔍 Extraire le texte", type="primary"):
            with st.spinner("📄 Extraction..."):
                filename = uploaded_file.name.lower()
                
                if filename.endswith(".pdf"):
                    text = extract_text_from_pdf(uploaded_file) if PDF_AVAILABLE else "❌ PyPDF2 non disponible"
                elif filename.endswith(".docx"):
                    text = extract_text_from_docx(uploaded_file) if DOCX_AVAILABLE else "❌ python-docx non disponible"
                else:
                    text = extract_text_from_txt(uploaded_file)
                
                st.session_state.extracted_text = text
        
        if "extracted_text" in st.session_state and st.session_state.extracted_text:
            text = st.session_state.extracted_text
            
            if not text.startswith("❌") and not text.startswith("⚠️"):
                word_count = len(text.split())
                char_count = len(text)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📝 Mots", f"{word_count:,}")
                with col2:
                    st.metric("🔤 Caractères", f"{char_count:,}")
                with col3:
                    st.metric("📄 Lignes", f"{text.count(chr(10)) + 1:,}")
                
                with st.expander("👁️ Aperçu (500 premiers caractères)"):
                    st.text(text[:500] + "...")
                
                st.markdown("---")
                st.markdown("### 🧠 Analyse IA du document")
                
                analysis_types = {
                    "📋 Résumé exécutif": "Crée un résumé concis et professionnel",
                    "🔍 Analyse détaillée": "Analyse approfondie point par point",
                    "• Points clés": "Liste les points essentiels en bullet points",
                    "❓ Q&A": "Génère des questions/réponses pertinentes",
                    "⚖️ Analyse juridique": "Identifie clauses et risques (contrats)",
                    "🏥 Analyse médicale": "Analyse clinique (dossiers médicaux)",
                    "💻 Code review": "Analyse qualité code, bugs, optimisations",
                    "📊 Extraction données": "Extrait données structurées (tableaux, chiffres)"
                }
                
                analysis_type = st.selectbox("Type d'analyse", list(analysis_types.keys()))
                custom_q = st.text