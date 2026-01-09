"""
MicroLLM Studio - Enterprise On-Premise AI Assistant
Version stable et sécurisée
"""

import os
import streamlit as st
from datetime import datetime
import PyPDF2
import docx

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="MicroLLM Studio",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# OPTIONAL: OpenAI SDK
# ===============================
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except Exception:
    OpenAI = None
    OPENAI_AVAILABLE = False

# ===============================
# SYSTEM INFO
# ===============================
SYSTEM_INFO = {
    "platform": "MicroLLM Studio",
    "version": "1.6.0-Stable",
    "base_model": "ARSLM / External LLM",
}

# ===============================
# DOMAINS
# ===============================
DOMAINS = {
    "💼 RH & Recrutement": "Tu es un expert RH et recrutement. Réponds de manière professionnelle et confidentielle.",
    "⚖️ Juridique & Compliance": "Tu es un assistant juridique. Réponses informatives uniquement, jamais de conseil légal.",
    "🏥 Médical & Santé": "Tu es un assistant médical pour professionnels de santé. Ne remplace jamais un avis médical.",
    "🔬 Recherche & Sciences": "Tu es un assistant de recherche scientifique rigoureux et factuel.",
    "💻 Développement & Code": "Tu es un expert en développement logiciel et architecture.",
    "📊 Analyse & Business Intelligence": "Tu es un expert data et business intelligence, orienté décisions.",
}

# ===============================
# SESSION STATE INIT
# ===============================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_domain" not in st.session_state:
    st.session_state.current_domain = "💼 RH & Recrutement"

if "doc_analyzed" not in st.session_state:
    st.session_state.doc_analyzed = False

# ===============================
# SIDEBAR - API CONFIG
# ===============================
st.sidebar.title("🔐 Configuration API")

# Clé sécurisée
api_key = st.secrets.get("OPENAI_API_KEY", None) if hasattr(st, 'secrets') else None

if not api_key:
    api_key = st.sidebar.text_input("Clé API OpenAI", type="password", help="Ajoutez votre clé OpenAI ici")

if api_key:
    st.sidebar.success("✅ Clé API configurée")
else:
    st.sidebar.warning("⚠️ Clé API manquante")

model_name = st.sidebar.selectbox(
    "Modèle",
    ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
    index=0
)

st.sidebar.markdown("---")

# Domain selection
selected_domain = st.sidebar.selectbox(
    "🎯 Domaine de spécialisation",
    list(DOMAINS.keys()),
    index=list(DOMAINS.keys()).index(st.session_state.current_domain)
)

# Update domain if changed
if selected_domain != st.session_state.current_domain:
    st.session_state.current_domain = selected_domain

st.sidebar.markdown("---")

# Clear chat button
if st.sidebar.button("🗑️ Effacer l'historique", use_container_width=True):
    st.session_state.messages = []
    st.session_state.doc_analyzed = False
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption(f"**Version:** {SYSTEM_INFO['version']}")
st.sidebar.caption("© 2025 Benjamin Amaad Kama")

# ===============================
# HEADER
# ===============================
st.markdown(
    f"""
    <div style="background:linear-gradient(135deg,#1e3c72,#667eea);
                padding:2rem;border-radius:12px;color:white;margin-bottom:2rem;">
        <h1 style="margin:0;">🤖 MicroLLM Studio</h1>
        <p style="margin:0.5rem 0 0 0;">Enterprise AI Assistant – API Secure Mode</p>
        <small>Version {SYSTEM_INFO['version']}</small>
    </div>
    """,
    unsafe_allow_html=True
)

# Status indicators
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Messages", len(st.session_state.messages))
with col2:
    st.metric("Domaine actif", st.session_state.current_domain.split()[0])
with col3:
    status = "✅ Connecté" if api_key and OPENAI_AVAILABLE else "❌ Non configuré"
    st.metric("API Status", status)

# ===============================
# AI ENGINE
# ===============================
def call_ai_api(user_query: str, domain: str) -> str:
    """Appelle l'API OpenAI avec gestion d'erreurs"""
    
    if not api_key:
        return "❌ **Erreur**: Clé API manquante. Configurez votre clé OpenAI dans la sidebar."

    if not OPENAI_AVAILABLE:
        return "❌ **Erreur**: SDK OpenAI non installé. Ajoutez `openai` dans requirements.txt"

    try:
        client = OpenAI(api_key=api_key)
        system_prompt = DOMAINS.get(domain, "Tu es un assistant professionnel.")

        # Construire l'historique
        messages = [{"role": "system", "content": system_prompt}]
        
        # Ajouter les 6 derniers messages (contexte limité)
        for msg in st.session_state.messages[-6:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Ajouter la nouvelle question
        messages.append({"role": "user", "content": user_query})

        # Appel API
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.3,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        error_msg = str(e)
        if "authentication" in error_msg.lower():
            return "❌ **Erreur d'authentification**: Vérifiez votre clé API OpenAI."
        elif "quota" in error_msg.lower():
            return "❌ **Quota dépassé**: Votre compte OpenAI a atteint sa limite. Vérifiez votre facturation."
        elif "rate_limit" in error_msg.lower():
            return "❌ **Limite de taux**: Trop de requêtes. Attendez quelques secondes."
        else:
            return f"❌ **Erreur API**: {error_msg}"

# ===============================
# PDF / DOCX / TXT EXTRACTION
# ===============================
def extract_text_from_file(uploaded_file):
    """Extrait le texte d'un fichier uploadé"""
    if uploaded_file is None:
        return ""
    
    filename = uploaded_file.name.lower()
    text = ""
    
    try:
        if filename.endswith(".pdf"):
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                    
        elif filename.endswith(".docx"):
            doc = docx.Document(uploaded_file)
            for para in doc.paragraphs:
                text += para.text + "\n"
                
        elif filename.endswith(".txt"):
            text = str(uploaded_file.read(), encoding="utf-8")
            
        else:
            return "Format non supporté. PDF, DOCX ou TXT uniquement."
            
    except Exception as e:
        return f"Erreur lors de l'extraction: {str(e)}"
    
    return text.strip()

# ===============================
# MAIN INTERFACE
# ===============================

# Tabs for different features
tab1, tab2 = st.tabs(["💬 Chat", "📄 Analyse de Documents"])

# ===== TAB 1: CHAT =====
with tab1:
    st.markdown(f"### 💬 Assistant {st.session_state.current_domain}")
    
    # Display chat history
    for idx, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            st.markdown(
                f"""<div style='background:#667eea;color:white;padding:1rem;
                border-radius:12px;margin:1rem 0 1rem 20%;'>
                <strong>👤 Vous:</strong><br>{msg['content']}</div>""",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""<div style='background:#f4f6f8;padding:1rem;border-radius:12px;
                margin:1rem 20% 1rem 0;border-left:4px solid #667eea;'>
                <strong>🤖 Assistant:</strong><br>{msg['content']}</div>""",
                unsafe_allow_html=True
            )
    
    # Chat input form
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Votre message",
            placeholder="Posez votre question…",
            height=100,
            key="chat_input_field"
        )
        
        submitted = st.form_submit_button("📤 Envoyer", use_container_width=True, type="primary")
        
        if submitted and user_input.strip():
            # Add user message
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
            
            # Get AI response
            with st.spinner("🤖 Génération de la réponse..."):
                answer = call_ai_api(user_input, st.session_state.current_domain)
            
            # Add assistant message
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })
            
            # Rerun to display new messages
            st.rerun()

# ===== TAB 2: DOCUMENT ANALYSIS =====
with tab2:
    st.markdown("### 📄 Analyse de Document")
    
    st.info("💡 **Astuce**: Uploadez un document PDF, DOCX ou TXT pour l'analyser avec l'IA.")
    
    uploaded_file = st.file_uploader(
        "Choisir un fichier",
        type=["pdf", "docx", "txt"],
        key="file_uploader_widget"
    )
    
    if uploaded_file:
        st.success(f"✅ Fichier chargé: **{uploaded_file.name}**")
        
        # Extract text button
        if st.button("🔍 Extraire le texte", key="extract_button"):
            with st.spinner("📄 Extraction du texte en cours..."):
                doc_text = extract_text_from_file(uploaded_file)
            
            if doc_text:
                st.session_state.extracted_text = doc_text
                st.success("✅ Texte extrait avec succès!")
        
        # Display extracted text
        if "extracted_text" in st.session_state and st.session_state.extracted_text:
            with st.expander("📝 Texte extrait", expanded=False):
                st.text_area(
                    "Contenu du document",
                    value=st.session_state.extracted_text,
                    height=300,
                    key="extracted_text_display",
                    disabled=True
                )
            
            # Analysis options
            st.markdown("---")
            st.markdown("### 🧠 Options d'analyse")
            
            analysis_type = st.selectbox(
                "Type d'analyse",
                [
                    "Résumé général",
                    "Analyse détaillée",
                    "Points clés (bullet points)",
                    "Questions/Réponses sur le document",
                    "Analyse juridique (si contrat)",
                    "Analyse médicale (si dossier médical)"
                ],
                key="analysis_type_select"
            )
            
            if st.button("🚀 Lancer l'analyse", key="analyze_button", type="primary"):
                analysis_prompt = f"""Voici un document à analyser:

{st.session_state.extracted_text[:4000]}

Type d'analyse demandée: {analysis_type}

Fournis une analyse {analysis_type.lower()} complète et structurée."""
                
                # Add to messages
                st.session_state.messages.append({
                    "role": "user",
                    "content": f"[Analyse de document] {analysis_type}"
                })
                
                # Get analysis
                with st.spinner("🤖 Analyse en cours..."):
                    answer = call_ai_api(analysis_prompt, st.session_state.current_domain)
                
                # Add response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })
                
                st.success("✅ Analyse terminée! Consultez l'onglet Chat pour voir les résultats.")
                st.session_state.doc_analyzed = True

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.markdown(
    f"""<div style='text-align:center;color:#666;'>
    © {datetime.now().year} MicroLLM Studio – Secure API Mode | 
    Contact: flywithjesus@outlook.com
    </div>""",
    unsafe_allow_html=True
)