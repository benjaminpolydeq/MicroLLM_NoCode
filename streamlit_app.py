"""
MicroLLM Studio - Ultra-light Streamlit Assistant
No-Code AI Assistant for sensitive, on-premise environments
Supports PDF, TXT, DOCX, lightweight chat & summaries
"""

import streamlit as st
import time
import PyPDF2
import docx

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="MicroLLM Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# CUSTOM CSS + ANIMATIONS
# ===============================
st.markdown("""
<style>
* { font-family: 'Inter', sans-serif; }

.main-header {
    font-size: 2.5rem; font-weight: bold;
    background: linear-gradient(90deg, #667eea, #764ba2);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    transition: all 0.4s ease;
}
.main-header:hover { transform: scale(1.05); }

.user-msg {
    background: #667eea; color: white;
    padding: 12px; border-radius: 12px;
    margin-left: 25%; margin-top: 10px;
    transition: transform 0.2s; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
.user-msg:hover { transform: scale(1.02); }

.assistant-msg {
    background: #f7f7f8; color: #1a1a1a;
    padding: 12px; border-radius: 12px;
    margin-right: 25%; margin-top: 10px;
    border-left: 4px solid #667eea; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    transition: transform 0.2s;
}
.assistant-msg:hover { transform: scale(1.02); }

.stButton button {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white; border-radius: 8px; padding: 8px 16px;
    font-weight: 600; transition: all 0.3s ease;
}
.stButton button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(102,126,234,0.4); }
</style>
""", unsafe_allow_html=True)

# ===============================
# SESSION STATE
# ===============================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/667eea/ffffff?text=MicroLLM", use_container_width=True)
    page = st.radio("Navigation", ["🏠 Dashboard", "💬 Chat"], label_visibility="collapsed")
    st.markdown("---")
    st.info("Ultra-light, On-Prem AI Assistant")

# ===============================
# FILE PROCESSING FUNCTIONS
# ===============================
def extract_text(file):
    """Extract text from PDF, DOCX, TXT"""
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        return "\n".join([page.extract_text() or "" for page in reader.pages])
    elif file.type == "text/plain":
        return file.read().decode("utf-8")
    elif file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    return ""

def summarize_text(text, max_sentences=5):
    """Ultra-light summary"""
    sentences = text.split(". ")
    return ". ".join(sentences[:max_sentences]) + ("..." if len(sentences) > max_sentences else text)

# ===============================
# DASHBOARD
# ===============================
if page == "🏠 Dashboard":
    st.markdown('<p class="main-header">MicroLLM Studio</p>', unsafe_allow_html=True)
    st.markdown("📄 Upload a document to analyze")

    uploaded_file = st.file_uploader("PDF, TXT, DOCX", type=["pdf","txt","docx"])
    if uploaded_file:
        with st.spinner("Extracting text..."):
            text_content = extract_text(uploaded_file)
            st.success("Text extracted!")
            st.text_area("Content", text_content, height=200)

        st.markdown("### ⏳ Analysis")
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i+1)

        st.markdown("### 📋 Summary")
        st.write(summarize_text(text_content))

# ===============================
# CHAT
# ===============================
elif page == "💬 Chat":
    st.markdown('<p class="main-header">MicroLLM Chat</p>', unsafe_allow_html=True)

    # Display previous messages
    for msg in st.session_state.messages:
        cls = "user-msg" if msg["role"]=="user" else "assistant-msg"
        st.markdown(f'<div class="{cls}">{msg["content"]}</div>', unsafe_allow_html=True)

    # Chat input
    user_input = st.chat_input("Ask MicroLLM...")
    if user_input:
        # Ultra-light local response (example: keyword matching)
        response = "🤖 I am your local AI assistant. I received: " + user_input
        if "summary" in user_input.lower():
            response += "\nTry uploading a document for automatic summaries."

        # Save messages
        st.session_state.messages.append({"role":"user","content":user_input})
        st.session_state.messages.append({"role":"assistant","content":response})
        st.rerun()