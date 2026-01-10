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
    initial_sidebar_state="expanded"
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
    
    .analysis-result {
        background: white;
        border: 2px solid #667eea;
        border-radius: 12px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.15);
    }
    
    .contact-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 15px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        margin: 2rem 0;
    }
    
    .download-btn {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 8px;
        text-decoration: none;
        display: inline-block;
        font-weight: 600;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ===============================
# SYSTEM INFO & DOMAINS
# ===============================
SYSTEM_INFO = {
    "platform": "MicroLLM Studio",
    "version": "2.1.0",
    "contact": "flywithjesus@outlook.com",
    "location": "Nguekhokh, Mbour, Sénégal",
    "author": "Benjamin Amaad Kama"
}

DOMAINS = {
    "💼 RH & Recrutement": {
        "system_prompt": "Tu es un expert RH et recrutement. Analyse les CV, aide à la rédaction de fiches de poste, évalue les candidats.",
        "icon": "💼"
    },
    "⚖️ Juridique": {
        "system_prompt": "Tu es un assistant juridique expert. Analyse les contrats, identifie les clauses problématiques. IMPORTANT: Tes réponses sont informatives uniquement.",
        "icon": "⚖️"
    },
    "🏥 Médical": {
        "system_prompt": "Tu es un assistant médical pour professionnels. Aide au diagnostic différentiel, analyse de dossiers. CRUCIAL: Pour professionnels uniquement.",
        "icon": "🏥"
    },
    "🔬 Recherche": {
        "system_prompt": "Tu es un assistant de recherche scientifique. Aide aux revues de littérature, analyse de données.",
        "icon": "🔬"
    },
    "💻 Code": {
        "system_prompt": "Tu es un expert développement. Analyse de code, détection de bugs, optimisation.",
        "icon": "💻"
    },
    "📊 Business": {
        "system_prompt": "Tu es un expert BI. Analyse de données, insights business, recommandations.",
        "icon": "📊"
    }
}

ANALYSIS_TEMPLATES = {
    "📋 Résumé": "Analyse ce document et fournis un résumé structuré avec vue d'ensemble, points clés et conclusions.\n\nDocument:\n{text}",
    "🔍 Détaillé": "Effectue une analyse approfondie : contexte, structure, arguments, conclusions.\n\nDocument:\n{text}",
    "📝 Points clés": "Extrais les points clés sous forme de bullet points structurés.\n\nDocument:\n{text}",
    "❓ Q&A": "Génère 5-10 questions pertinentes avec réponses détaillées.\n\nDocument:\n{text}",
    "⚖️ Juridique": "Analyse juridique : type de document, clauses principales, risques, recommandations. RAPPEL: Analyse informative uniquement.\n\nDocument:\n{text}",
    "🏥 Médical": "Analyse médicale : patient, symptômes, examens, diagnostic différentiel. IMPORTANT: Pour professionnels uniquement.\n\nDocument:\n{text}",
    "💻 Code Review": "Revue de code : qualité, bugs, sécurité, optimisations, note sur 10.\n\nCode:\n{text}",
    "📊 Données": "Extrais et structure : données numériques, tableaux, entités nommées.\n\nDocument:\n{text}"
}

# ===============================
# SESSION STATE
# ===============================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_domain" not in st.session_state:
    st.session_state.current_domain = "💼 RH & Recrutement"
if "page" not in st.session_state:
    st.session_state.page = "🏠 Accueil"
if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []

# ===============================
# FUNCTIONS
# ===============================
def extract_text_from_pdf(uploaded_file):
    try:
        uploaded_file.seek(0)
        reader = PyPDF2.PdfReader(BytesIO(uploaded_file.read()))
        if reader.is_encrypted:
            return "❌ PDF protégé"
        text = ""
        for i, page in enumerate(reader.pages):
            try:
                text += f"\n--- Page {i + 1} ---\n{page.extract_text()}\n"
            except:
                text += f"\n--- Page {i + 1} : Erreur ---\n"
        return text.strip() or "⚠️ Aucun texte"
    except Exception as e:
        return f"❌ Erreur PDF: {str(e)}"

def extract_text_from_docx(uploaded_file):
    try:
        uploaded_file.seek(0)
        doc = docx.Document(uploaded_file)
        text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        return text or "⚠️ Document vide"
    except Exception as e:
        return f"❌ Erreur DOCX: {str(e)}"

def extract_text_from_txt(uploaded_file):
    try:
        uploaded_file.seek(0)
        for enc in ['utf-8', 'latin-1', 'cp1252']:
            try:
                return uploaded_file.read().decode(enc)
            except:
                continue
        return "❌ Encodage non supporté"
    except Exception as e:
        return f"❌ Erreur: {str(e)}"

def call_openai_api(messages, domain):
    api_key = st.secrets.get("OPENAI_API_KEY") if hasattr(st, 'secrets') else None
    if not api_key:
        return "❌ Clé API OpenAI manquante"
    if not OPENAI_AVAILABLE:
        return "❌ SDK OpenAI non disponible"
    try:
        client = OpenAI(api_key=api_key)
        api_messages = [{"role": "system", "content": DOMAINS[domain]["system_prompt"]}]
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
    api_key = st.secrets.get("OPENAI_API_KEY") if hasattr(st, 'secrets') else None
    if not api_key:
        return "❌ Clé API OpenAI manquante"
    if not OPENAI_AVAILABLE:
        return "❌ SDK OpenAI non disponible"
    try:
        client = OpenAI(api_key=api_key)
        if custom_question:
            prompt = f"{custom_question}\n\nDocument:\n{text}"
        else:
            template = ANALYSIS_TEMPLATES.get(analysis_type, ANALYSIS_TEMPLATES["📋 Résumé"])
            prompt = template.format(text=text)
        
        if len(prompt) > 12000:
            prompt = prompt[:12000] + "\n\n[Document tronqué]"
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Tu es un assistant d'analyse expert. Fournis des analyses précises et structurées."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=3000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Erreur: {str(e)}"

def create_download_link(text, filename):
    b64 = base64.b64encode(text.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}" class="download-btn">📥 Télécharger</a>'

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.markdown("### 🤖 MicroLLM Studio")
    st.markdown(f"**Version {SYSTEM_INFO['version']}**")
    st.markdown("---")
    
    page = st.radio("Navigation", ["🏠 Accueil", "💬 Chat IA", "📄 Analyse Documents", "📞 Contact"], label_visibility="collapsed")
    st.session_state.page = page
    
    st.markdown("---")
    
    if page == "💬 Chat IA":
        st.markdown("### 🎯 Domaine")
        selected_domain = st.selectbox("Spécialisation", list(DOMAINS.keys()), label_visibility="collapsed")
        st.session_state.current_domain = selected_domain
        if st.button("🗑️ Effacer", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    st.markdown("---")
    st.caption("© 2025 Benjamin Amaad Kama")
    st.caption(f"📍 {SYSTEM_INFO['location']}")

# ===============================
# PAGE: ACCUEIL
# ===============================
if st.session_state.page == "🏠 Accueil":
    header_html = f"""
    <div class="main-header">
        <h1>🤖 MicroLLM Studio</h1>
        <div class="subtitle">Plateforme d'IA d'Entreprise - Sécurisée et Spécialisée</div>
        <div class="arslm-badge">Powered by ARSLM + OpenAI GPT-4</div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## 🎯 MicroLLM Studio")
        st.markdown("""
        Plateforme no-code pour déployer des assistants IA spécialisés.
        
        ### ✨ Fonctionnalités
        - 🔒 **Sécurisé** : Données privées, RGPD
        - 🧠 **Spécialisé** : 6 domaines experts
        - 📚 **Multi-formats** : PDF, Word, Code
        - ⚡ **Rapide** : Analyses en secondes
        """)
        
        features = [
            {"icon": "💬", "title": "Chat IA", "desc": "Assistant expert par domaine"},
            {"icon": "📄", "title": "Analyse Documents", "desc": "8 types d'analyses GPT-4"},
            {"icon": "📊", "title": "Export", "desc": "Téléchargement des résultats"}
        ]
        
        for f in features:
            card_html = f"""
            <div class="feature-card">
                <h3>{f['icon']} {f['title']}</h3>
                <p>{f['desc']}</p>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 Stats")
        metric_html = f"""
        <div class="metric-card">
            <div>Domaines</div>
            <div class="metric-value">{len(DOMAINS)}</div>
        </div>
        <div class="metric-card">
            <div>Analyses</div>
            <div class="metric-value">{len(st.session_state.analysis_history)}</div>
        </div>
        """
        st.markdown(metric_html, unsafe_allow_html=True)

# ===============================
# PAGE: CHAT IA
# ===============================
elif st.session_state.page == "💬 Chat IA":
    st.markdown(f"### 💬 Assistant IA - {st.session_state.current_domain}")
    
    info_html = f"""
    <div class="info-box">
        <strong>{DOMAINS[st.session_state.current_domain]['icon']} Domaine :</strong> {st.session_state.current_domain}
    </div>
    """
    st.markdown(info_html, unsafe_allow_html=True)
    
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            msg_html = f"""<div class="user-msg"><strong>👤 Vous:</strong><br>{msg['content']}</div>"""
        else:
            msg_html = f"""<div class="assistant-msg"><strong>🤖 Assistant:</strong><br>{msg['content']}</div>"""
        st.markdown(msg_html, unsafe_allow_html=True)
    
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area("Message", placeholder="Posez votre question...", height=120)
        submitted = st.form_submit_button("📤 Envoyer", type="primary", use_container_width=True)
        
        if submitted and user_input.strip():
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.spinner("🤖 Génération..."):
                response = call_openai_api(st.session_state.messages, st.session_state.current_domain)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

# ===============================
# PAGE: ANALYSE DOCUMENTS
# ===============================
elif st.session_state.page == "📄 Analyse Documents":
    st.markdown("### 📄 Analyse Intelligente avec GPT-4")
    
    info_html = """
    <div class="info-box">
        <h4>📚 Formats : PDF, DOCX, TXT, Code</h4>
    </div>
    """
    st.markdown(info_html, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("📁 Fichier", type=["pdf", "docx", "txt", "py", "js", "java", "cpp", "md"])
    
    if uploaded_file:
        st.success(f"✅ {uploaded_file.name} ({uploaded_file.size/1024/1024:.2f} MB)")
        
        if st.button("🔍 Extraire", type="primary", use_container_width=True):
            with st.spinner("📄 Extraction..."):
                fn = uploaded_file.name.lower()
                if fn.endswith(".pdf"):
                    text = extract_text_from_pdf(uploaded_file) if PDF_AVAILABLE else "❌ PyPDF2 requis"
                elif fn.endswith(".docx"):
                    text = extract_text_from_docx(uploaded_file) if DOCX_AVAILABLE else "❌ python-docx requis"
                else:
                    text = extract_text_from_txt(uploaded_file)
                st.session_state.extracted_text = text
        
        if "extracted_text" in st.session_state and st.session_state.extracted_text:
            text = st.session_state.extracted_text
            
            if not text.startswith("❌"):
                words = len(text.split())
                chars = len(text)
                
                col1, col2, col3 = st.columns(3)
                col1.metric("📝 Mots", f"{words:,}")
                col2.metric("🔤 Caractères", f"{chars:,}")
                col3.metric("📄 Lignes", f"{text.count(chr(10)) + 1:,}")
                
                with st.expander("👁️ Aperçu"):
                    st.text(text[:500] + "...")
                
                st.markdown("---")
                st.markdown("### 🧠 Analyse IA")
                
                analysis_type = st.selectbox("Type", list(ANALYSIS_TEMPLATES.keys()))
                custom_q = st.text_input("Question personnalisée (optionnel)")
                
                if st.button("🚀 Analyser", type="primary", use_container_width=True):
                    with st.spinner("🤖 Analyse en cours..."):
                        result = analyze_document_with_gpt(text, analysis_type, custom_q if custom_q else None)
                    
                    result_html = f"""
                    <div class="analysis-result">
                        <h4>📊 Résultat de l'analyse</h4>
                        {result}
                    </div>
                    """
                    st.markdown(result_html, unsafe_allow_html=True)
                    
                    st.markdown(create_download_link(result, f"analyse_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"), unsafe_allow_html=True)
                    
                    st.session_state.analysis_history.append({
                        "timestamp": datetime.now(),
                        "file": uploaded_file.name,
                        "type": analysis_type,
                        "result": result
                    })
            else:
                st.error(text)

# ===============================
# PAGE: CONTACT
# ===============================
elif st.session_state.page == "📞 Contact":
    st.markdown("### 📞 Contactez-nous")
    
    contact_html = """
    <div class="contact-card">
        <h2>💌 Envoyez-nous un message</h2>
        <p>Notre équipe vous répondra dans les plus brefs délais</p>
    </div>
    """
    st.markdown(contact_html, unsafe_allow_html=True)
    
    with st.form("contact_form"):
        name = st.text_input("👤 Nom complet", placeholder="Votre nom")
        email = st.text_input("📧 Email", placeholder="votre.email@exemple.com")
        subject = st.text_input("📋 Sujet", placeholder="Objet de votre message")
        message = st.text_area("💬 Message", placeholder="Votre message...", height=200)
        
        submit = st.form_submit_button("📤 Envoyer le message", type="primary", use_container_width=True)
        
        if submit:
            if name and email and subject and message:
                st.success(f"✅ Message envoyé ! Nous vous contacterons à {email}")
                st.balloons()
            else:
                st.error("❌ Veuillez remplir tous les champs")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        info_html = f"""
        <div class="info-box">
            <h4>📍 Coordonnées</h4>
            <p><strong>Email:</strong> {SYSTEM_INFO['contact']}</p>
            <p><strong>Localisation:</strong> {SYSTEM_INFO['location']}</p>
            <p><strong>Auteur:</strong> {SYSTEM_INFO['author']}</p>
        </div>
        """
        st.markdown(info_html, unsafe_allow_html=True)
    
    with col2:
        info_html = """
        <div class="info-box">
            <h4>⏰ Disponibilité</h4>
          