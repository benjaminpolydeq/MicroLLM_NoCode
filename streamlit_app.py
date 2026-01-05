"""
MicroLLM Studio - ARSLM Smart Version with Document Summarizer
No PyTorch dependencies - Pure Python implementation
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import json
import os
import PyPDF2
import docx
import re

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
# ARSLM INFO
# ===============================
ARSLM_INFO = {
    "name": "ARSLM",
    "version": "1.2.0-Smart",
    "description": (
        "ARSLM – Lightweight, Efficient & Secure AI\n"
        "Small language model with context-aware chat and document summarization. "
        "Runs on low-resource environments, ensures data privacy, and provides "
        "intelligent text generation and document insights."
    )
}

# ===============================
# CUSTOM CSS
# ===============================
st.markdown("""
<style>
.main-header { font-size:3rem; font-weight:bold; background: linear-gradient(90deg,#667eea 0%,#764ba2 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.metric-card { background:linear-gradient(135deg,#667eea 0%,#764ba2 100%); padding:20px; border-radius:15px; color:white; text-align:center; box-shadow:0px 5px 15px rgba(0,0,0,0.2); transition:transform 0.2s; cursor:pointer; margin:5px 0; }
.metric-card:hover { transform: scale(1.05); }
.user-msg { background:#e0f7fa; padding:10px; border-radius:10px; text-align:right; margin:5px 0; }
.assistant-msg { background:#f3e5f5; padding:10px; border-radius:10px; text-align:left; margin:5px 0; }
.info-box { background:linear-gradient(135deg,rgba(102,126,234,0.1)0%,rgba(118,75,162,0.1)100%); border-left:4px solid #667eea; padding:15px; border-radius:8px; margin:15px 0; }
.suggestion-btn { background:#667eea; color:white; border:none; border-radius:8px; padding:5px 10px; margin:3px; cursor:pointer; }
.suggestion-btn:hover { background:#764ba2; }
</style>
""", unsafe_allow_html=True)

# ===============================
# ARSLM ENGINE
# ===============================
class ARSLMEngine:
    """Lightweight ARSLM engine with context-aware responses and document summarization"""
    
    def __init__(self):
        self.knowledge_base = [
            {"keywords":["arslm","what is"], "response":"ARSLM est un moteur AI léger pour chat et génération de texte."},
            {"keywords":["pricing","tarif"], "response":"Plans : Gratuit, Starter $99, Pro $299, Enterprise sur devis."},
            {"keywords":["features","fonctionnalités"], "response":"Fonctionnalités : Chat contextuel, mémoire, déploiement local ou cloud."},
            {"keywords":["install","setup"], "response":"Installation : Clonez le repo, pip install -r requirements.txt, puis streamlit run streamlit_app.py."},
            {"keywords":["support","help"], "response":"Support : benjokama@hotmail.fr"}
        ]
        self.conversation_history = []
        self.document_context = []

    def ingest_documents(self, texts):
        """Store document texts for context-aware chat"""
        self.document_context = texts

    def summarize_documents(self):
        """Very simple heuristic summarizer"""
        summaries = []
        for doc in self.document_context:
            sentences = re.split(r'(?<=[.!?]) +', doc)
            if len(sentences) <= 5:
                summaries.append(" ".join(sentences))
            else:
                # pick first, middle, last sentence as simple summary
                summaries.append(" ".join([sentences[0], sentences[len(sentences)//2], sentences[-1]]))
        return summaries

    def generate_response(self, query):
        """Generate a context-aware response"""
        query_lower = query.lower()
        response = None

        # Knowledge base matching
        best_match = None
        best_score = 0
        for item in self.knowledge_base:
            score = sum(1 for kw in item["keywords"] if kw in query_lower)
            if score > best_score:
                best_score = score
                best_match = item

        if best_match:
            response = best_match["response"]
        else:
            # Context-aware fallback
            response = "🤔 Je n'ai pas de réponse spécifique pour cette question."
            if self.document_context:
                combined_text = "\n".join(self.document_context)
                sentences = re.split(r'(?<=[.!?]) +', combined_text)
                matched_sentences = [s for s in sentences if any(w in s.lower() for w in query_lower.split())]
                if matched_sentences:
                    response = "📄 Context-based answer:\n" + " ".join(matched_sentences[:3])

        # Store conversation
        self.conversation_history.append({
            "query": query,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
        return response

    def suggest_questions(self):
        """Generate simple suggested questions based on context"""
        suggestions = ["Qu'est-ce que ARSLM ?", "Quels sont les tarifs ?", "Quelles sont les fonctionnalités ?", "Comment installer ARSLM ?"]
        if self.document_context:
            suggestions.append("Peux-tu résumer ce document ?")
        return suggestions[:5]

# ===============================
# SESSION STATE
# ===============================
if "engine" not in st.session_state:
    st.session_state.engine = ARSLMEngine()
if "messages" not in st.session_state:
    st.session_state.messages = []

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/667eea/ffffff?text=MicroLLM", width=200)
    page = st.radio("Navigation", ["🏠 Dashboard", "💬 Chat", "📊 Analytics", "⚙️ Settings"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("### System Status")
    st.success("🟢 Active")
    st.markdown(f"**Conversations:** {len(st.session_state.messages)}")
    st.markdown(f"**Documents Loaded:** {len(st.session_state.engine.document_context)}")

# ===============================
# DASHBOARD
# ===============================
if page == "🏠 Dashboard":
    st.markdown('<p class="main-header">MicroLLM Studio</p>', unsafe_allow_html=True)
    st.caption("Lightweight AI – Context-Aware, No-Code")
    st.markdown("### About ARSLM")
    st.markdown(f'<div class="info-box">{ARSLM_INFO["description"]}</div>', unsafe_allow_html=True)

# ===============================
# CHAT + DOCUMENTS
# ===============================
elif page == "💬 Chat":
    st.markdown('<p class="main-header">MicroLLM Smart Chat</p>', unsafe_allow_html=True)
    st.caption(f"Chatting with {ARSLM_INFO['name']} – Lightweight, Context-Aware")

    # Upload documents
    with st.expander("📄 Upload documents"):
        uploaded_files = st.file_uploader("Upload files", type=["txt","pdf","csv","docx"], accept_multiple_files=True)
        document_texts = []
        if uploaded_files:
            for f in uploaded_files:
                st.success(f"Loaded: {f.name}")
                if f.type=="text/plain":
                    document_texts.append(f.read().decode("utf-8"))
                elif f.type=="application/pdf":
                    pdf_reader = PyPDF2.PdfReader(f)
                    text = "".join([page.extract_text() or "" for page in pdf_reader.pages])
                    document_texts.append(text)
                elif f.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document","application/msword"]:
                    doc = docx.Document(f)
                    text = "\n".join([p.text for p in doc.paragraphs])
                    document_texts.append(text)
                elif f.type=="text/csv":
                    df = pd.read_csv(f)
                    document_texts.append(df.to_csv(index=False))
        st.session_state.engine.ingest_documents(document_texts)

    # Summarize documents
    if document_texts:
        summaries = st.session_state.engine.summarize_documents()
        st.markdown("### 📝 Document Summaries")
        for i, s in enumerate(summaries):
            st.markdown(f"**Document {i+1} Summary:** {s}")

    # Display chat history
    for msg in st.session_state.messages:
        if msg["role"]=="user":
            st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-msg">{msg["content"]}</div>', unsafe_allow_html=True)

    # Suggested questions
    st.markdown("### 💡 Suggested Questions")
    suggestions = st.session_state.engine.suggest_questions()
    for s in suggestions:
        if st.button(s, key=s):
            st.session_state.messages.append({"role":"user","content":s})
            response = st.session_state.engine.generate_response(s)
            st.session_state.messages.append({"role":"assistant","content":response})
            st.rerun()

    # User input
    user_input = st.chat_input("Ask ARSLM...")
    if user_input:
        st.session_state.messages.append({"role":"user","content":user_input})
        response = st.session_state.engine.generate_response(user_input)
        st.session_state.messages.append({"role":"assistant","content":response})
        st.markdown(f'<div class="assistant-msg">{response}</div>', unsafe_allow_html=True)

# ===============================
# ANALYTICS
# ===============================
elif page == "📊 Analytics":
    st.markdown('<p class="main-header">Analytics</p>', unsafe_allow_html=True)
    st.caption("Visualize conversation history")
    history = st.session_state.engine.conversation_history
    if not history:
        st.info("No conversations yet.")
    else:
        df = pd.DataFrame(history)
        st.dataframe(df, use_container_width=True)
        if st.button("💾 Export JSON"):
            st.download_button(
                "Download JSON",
                data=json.dumps(history, indent=2, ensure_ascii=False),
                file_name=f"arslm_conversations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

# ===============================
# SETTINGS
# ===============================
elif page == "⚙️ Settings":
    st.markdown('<p class="main-header">Settings</p>', unsafe_allow_html=True)
    st.checkbox("Enable encryption", value=True)
    st.checkbox("Audit logging", value=True)

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;color:#777">
MicroLLM Studio v{ARSLM_INFO['version']} · Built on ARSLM · Context-Aware & Summarizer<br>
© 2025 Benjamin Amaad Kama
</div>
""", unsafe_allow_html=True)