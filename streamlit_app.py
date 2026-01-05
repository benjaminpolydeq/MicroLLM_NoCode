import streamlit as st
from langdetect import detect
import PyPDF2
import docx
import time
from tqdm import tqdm

# =====================
# PAGE CONFIG
# =====================
st.set_page_config(
    page_title="ARSLM – Lightweight, Efficient & Secure AI",
    page_icon="🧠",
    layout="wide"
)

# =====================
# CSS (léger & animé)
# =====================
st.markdown("""
<style>
.main-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(90deg,#4f46e5,#9333ea);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.card {
    background: #111827;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
}
.fade {
    animation: fadeIn 0.8s ease-in-out;
}
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# =====================
# HEADER
# =====================
st.markdown('<div class="main-title">ARSLM</div>', unsafe_allow_html=True)
st.markdown("""
**ARSLM – Lightweight, Efficient & Secure AI**  
Compact Small Language Model designed for real-world, privacy-first applications.
""")

# =====================
# FILE UPLOAD
# =====================
uploaded_file = st.file_uploader(
    "📄 Upload PDF, TXT or DOCX",
    type=["pdf", "txt", "docx"]
)

def extract_text(file):
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        return " ".join(page.extract_text() or "" for page in reader.pages)

    if file.type == "text/plain":
        return file.read().decode("utf-8", errors="ignore")

    if file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        d = docx.Document(file)
        return " ".join(p.text for p in d.paragraphs)

    return ""

def summarize(text):
    sentences = text.split(".")
    return ". ".join(sentences[:5]).strip() + "."

def extract_title(text):
    lines = [l.strip() for l in text.split("\n") if len(l.strip()) > 10]
    return lines[0] if lines else "Titre non détecté"

def key_points(text):
    sentences = text.split(".")
    return sentences[:8]

# =====================
# PROCESS DOCUMENT
# =====================
if uploaded_file:
    with st.spinner("📖 Analyzing document..."):
        text = extract_text(uploaded_file)
        time.sleep(0.5)

    lang = detect(text)

    st.progress(100)

    st.markdown("### 📌 Document title")
    st.markdown(f"<div class='card fade'>{extract_title(text)}</div>", unsafe_allow_html=True)

    st.markdown("### 🧾 Summary")
    st.markdown(f"<div class='card fade'>{summarize(text)}</div>", unsafe_allow_html=True)

    st.markdown("### 🔑 Key information")
    for point in key_points(text):
        st.markdown(f"- {point.strip()}")

# =====================
# CHAT DOCUMENT
# =====================
st.markdown("### 💬 Ask questions about the document")

if "chat" not in st.session_state:
    st.session_state.chat = []

question = st.chat_input("Ask a question about the document...")

if question and uploaded_file:
    st.session_state.chat.append(("user", question))

    q = question.lower()
    if "title" in q or "titre" in q:
        answer = extract_title(text)
    elif "summary" in q or "résumé" in q:
        answer = summarize(text)
    elif "key" in q or "clé" in q:
        answer = "\n".join(key_points(text))
    else:
        answer = "This question cannot be answered precisely from the document."

    st.session_state.chat.append(("assistant", answer))

for role, msg in st.session_state.chat:
    if role == "user":
        st.markdown(f"👤 **You:** {msg}")
    else:
        st.markdown(f"🤖 **ARSLM:** {msg}")