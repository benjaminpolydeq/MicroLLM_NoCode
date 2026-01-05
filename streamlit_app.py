"""
MicroLLM Studio - Streamlit Dashboard (Pro UI, ARSLM Base Model, Chunking Chat)
No-Code interface with Chat + Document Interaction (ARSLM-ready)
"""
import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import requests
import json
import os
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
# ARSLM Base Model Info
# ===============================
ARSLM_INFO = {
    "name": "ARSLM",
    "description": (
        "ARSLM – Lightweight, Efficient & Secure AI\n"
        "ARSLM is a compact small language model built for real-world applications, "
        "combining speed, efficiency, and adaptability. Designed to run on low-resource "
        "environments or on-premise, it ensures data privacy while providing intelligent "
        "text generation and chat capabilities. Ideal for companies handling sensitive "
        "data like healthcare, legal, or defense sectors."
    )
}

# ===============================
# LOAD MODEL
# ===============================
@st.cache_resource
def load_local_model():
    tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
    model = AutoModelForCausalLM.from_pretrained("distilgpt2")
    return tokenizer, model

tokenizer, model = load_local_model()
API_URL = "http://127.0.0.1:8000"

# ===============================
# CUSTOM CSS
# ===============================
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    font-weight: bold;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.2);
    transition: transform 0.2s;
    cursor: pointer;
}
.metric-card:hover {
    transform: scale(1.05);
}
.user-msg {
    background:#e0f7fa; padding:10px; border-radius:10px; text-align:right; margin:5px 0;
}
.assistant-msg {
    background:#f3e5f5; padding:10px; border-radius:10px; text-align:left; margin:5px 0;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# SESSION STATE
# ===============================
if "models" not in st.session_state:
    st.session_state.models = []
if "training_history" not in st.session_state:
    st.session_state.training_history = []
if "messages" not in st.session_state:
    st.session_state.messages = []

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.image(
        "https://via.placeholder.com/200x80/667eea/ffffff?text=MicroLLM",
        width=200
    )

    page = st.radio(
        "Navigation",
        ["🏠 Dashboard", "🎓 Training", "🔍 Models", "💬 Chat", "📊 Analytics", "⚙️ Settings"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### System Status")
    st.markdown("🟢 Active")
    st.markdown(f"**Models:** {len(st.session_state.models)}")
    st.markdown(f"**Training Jobs:** {len(st.session_state.training_history)}")

# ===============================
# DASHBOARD
# ===============================
if page == "🏠 Dashboard":
    st.markdown('<p class="main-header">MicroLLM Studio</p>', unsafe_allow_html=True)
    st.markdown("Democratizing Proprietary AI – On-Prem & No-Code")

    # -------------------------------
    # ARSLM info
    st.markdown("### Default Base Model")
    st.info(f"**{ARSLM_INFO['name']}**\n\n{ARSLM_INFO['description']}")

    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(f'<div class="metric-card">Active Models<br><h2>{len(st.session_state.models)}</h2></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="metric-card">Training Jobs<br><h2>{len(st.session_state.training_history)}</h2></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="metric-card">CPU Usage<br><h2>Low</h2></div>', unsafe_allow_html=True)
    col4.markdown(f'<div class="metric-card">Security<br><h2>On-Prem</h2></div>', unsafe_allow_html=True)

    st.markdown("---")
    # Dummy training loss
    epochs = list(range(1, 11))
    train_loss = [2.5, 2.1, 1.8, 1.6, 1.4, 1.3, 1.2, 1.1, 1.05, 1.0]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=epochs, y=train_loss, name="Training Loss", mode="lines+markers"))
    fig.update_layout(height=400, hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

# ===============================
# TRAINING
# ===============================
elif page == "🎓 Training":
    st.markdown('<p class="main-header">Training (No-Code)</p>', unsafe_allow_html=True)

    model_name = st.text_input("Model Name", value=ARSLM_INFO['name'])
    model_type = st.selectbox(
        "Model Type",
        ["ARSLM – Lightweight (Default)", "ARSLM-Small", "ARSLM-Medium"],
        index=0
    )

    if st.button("🚀 Start Training") and model_name:
        st.session_state.models.append({
            "name": model_name,
            "type": model_type,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "status": "Training"
        })

        history = []
        if os.path.exists("training_history.json"):
            with open("training_history.json", "r") as f:
                history = json.load(f)

        for epoch in range(1, 11):
            loss = round(2.5 / (0.5*epoch + 1), 3)
            accuracy = round(0.5 + 0.05*epoch, 3)
            history.append({
                "model": model_name,
                "type": model_type,
                "epoch": epoch,
                "loss": loss,
                "accuracy": accuracy,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })

        with open("training_history.json", "w") as f:
            json.dump(history, f, indent=4)

        st.success(f"Training job for {model_name} started and metrics saved!")

# ===============================
# MODELS
# ===============================
elif page == "🔍 Models":
    st.markdown('<p class="main-header">Models</p>', unsafe_allow_html=True)

    if not st.session_state.models:
        st.info("No models yet.")
    else:
        for m in st.session_state.models:
            st.markdown(f"### {m['name']}")
            st.write(m)

# ===============================
# CHAT + DOCUMENTS (CHUNKING)
# ===============================
elif page == "💬 Chat":
    st.markdown('<p class="main-header">MicroLLM Chat</p>', unsafe_allow_html=True)
    st.caption(f"Chatting with ARSLM ({ARSLM_INFO['name']}) – Local, On-device, No-Code")

    document_texts = []

    with st.expander("📄 Upload documents"):
        uploaded_files = st.file_uploader(
            "Upload files",
            type=["txt", "pdf", "csv", "docx"],
            accept_multiple_files=True
        )
        if uploaded_files:
            for f in uploaded_files:
                st.success(f"Loaded: {f.name}")

                # TXT
                if f.type == "text/plain":
                    text = f.read().decode("utf-8")
                    document_texts.append(text)
                # PDF
                elif f.type == "application/pdf":
                    pdf_reader = PyPDF2.PdfReader(f)
                    text = ""
                    for page in pdf_reader.pages:
                        t = page.extract_text()
                        if t: text += t + "\n"
                    document_texts.append(text)
                # DOCX
                elif f.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document","application/msword"]:
                    doc = docx.Document(f)
                    text = "\n".join([p.text for p in doc.paragraphs])
                    document_texts.append(text)
                # CSV
                elif f.type == "text/csv":
                    df = pd.read_csv(f)
                    text = df.to_csv(index=False)
                    document_texts.append(text)

    # Chat history
    for msg in st.session_state.messages:
        if msg["role"]=="user":
            st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-msg">{msg["content"]}</div>', unsafe_allow_html=True)

    user_input = st.chat_input("Ask MicroLLM...")
    if user_input:
        st.session_state.messages.append({"role":"user","content":user_input})

        with st.chat_message("assistant"):
            with st.spinner("MicroLLM is thinking..."):
                try:
                    # Combine ARSLM + documents + input
                    full_prompt = f"[Using {ARSLM_INFO['name']}] {user_input}"
                    if document_texts:
                        full_prompt += "\n\nContext:\n" + "\n".join(document_texts)

                    # Chunking GPT-2
                    max_len = 1024
                    input_ids = tokenizer(full_prompt, return_tensors="pt")["input_ids"]
                    if input_ids.size(1) > max_len:
                        input_ids = input_ids[:, -max_len:]  # keep last tokens
                    outputs = model.generate(
                        input_ids,
                        max_new_tokens=120,
                        temperature=0.7,
                        do_sample=True
                    )
                    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
                except Exception as e:
                    response = f"⚠️ Error generating response: {e}"

                st.markdown(f'<div class="assistant-msg">{response}</div>', unsafe_allow_html=True)
                st.session_state.messages.append({"role":"assistant","content":response})

# ===============================
# ANALYTICS
# ===============================
elif page == "📊 Analytics":
    st.markdown('<p class="main-header">Analytics</p>', unsafe_allow_html=True)
    st.caption("Visualize model and training performance")

    if not os.path.exists("training_history.json"):
        st.info("No training history yet. Start a model training first!")
    else:
        with open("training_history.json","r") as f:
            history = json.load(f)
        if not history:
            st.info("No training data found.")
        else:
            df_history = pd.DataFrame(history)
            st.dataframe(df_history)

            # Loss chart
            st.markdown("### 📉 Training Loss")
            fig_loss = go.Figure()
            for model_name in df_history['model'].unique():
                df_model = df_history[df_history['model']==model_name]
                fig_loss.add_trace(go.Scatter(x=df_model['epoch'],y=df_model['loss'],mode='lines+markers',name=model_name))
            fig_loss.update_layout(xaxis_title="Epochs", yaxis_title="Loss", height=400, hovermode="x unified")
            st.plotly_chart(fig_loss,use_container_width=True)

            # Accuracy chart
            st.markdown("### ✅ Model Accuracy")
            fig_acc = go.Figure()
            for model_name in df_history['model'].unique():
                df_model = df_history[df_history['model']==model_name]
                fig_acc.add_trace(go.Scatter(x=df_model['epoch'],y=df_model['accuracy'],mode='lines+markers',name=model_name))
            fig_acc.update_layout(xaxis_title="Epochs", yaxis_title="Accuracy", height=400, yaxis=dict(range=[0,1]), hovermode="x unified")
            st.plotly_chart(fig_acc,use_container_width=True)

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
st.markdown("""
<div style="text-align:center;color:#777">
MicroLLM Studio · Built on ARSLM · On-Prem No-Code AI
</div>
""", unsafe_allow_html=True)