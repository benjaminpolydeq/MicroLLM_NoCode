"""
MicroLLM Studio - Streamlit Dashboard + Chat
CPU-light version using DistilGPT2 (HuggingFace)
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time
import os
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# ----------------- Page Configuration -----------------
st.set_page_config(
    page_title="MicroLLM Studio",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- Custom CSS -----------------
st.markdown("""
<style>
    .main-header {font-size:3rem; font-weight:bold;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom:0.5rem;}
    .metric-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding:20px; border-radius:10px; color:white; margin:10px 0;}
</style>
""", unsafe_allow_html=True)

# ----------------- Session State -----------------
if 'training_history' not in st.session_state: st.session_state.training_history = []
if 'models' not in st.session_state: st.session_state.models = []
if 'active_training' not in st.session_state: st.session_state.active_training = False
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# ----------------- Sidebar -----------------
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/667eea/ffffff?text=MicroLLM", width=200)
    st.markdown("---")
    page = st.radio("Navigation",
                    ["🏠 Dashboard", "🎓 Training", "🔍 Models", "💬 Chat", "📊 Analytics", "⚙️ Settings"],
                    label_visibility="collapsed")
    st.markdown("---")
    st.markdown(f"**Status:** {'🟢 Active' if st.session_state.active_training else '⚪ Idle'}")
    st.markdown(f"**Models:** {len(st.session_state.models)}")
    st.markdown(f"**Training Jobs:** {len(st.session_state.training_history)}")

# ----------------- Dashboard -----------------
if page == "🏠 Dashboard":
    st.markdown('<p class="main-header">MicroLLM Studio Dashboard</p>', unsafe_allow_html=True)
    st.markdown("Democratizing Proprietary AI - Train specialized language models on limited private data")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Active Models", len(st.session_state.models), delta="+2 this week")
    col2.metric("Training Jobs", len(st.session_state.training_history), delta="3 completed")
    col3.metric("GPU Usage", "0%", delta="-")  # CPU only
    col4.metric("Avg. Accuracy", "87.3%", delta="+2.1%")
    
    st.markdown("---")
    st.subheader("📈 Training Progress Example")
    epochs = list(range(1, 11))
    train_loss = [2.5,2.1,1.8,1.6,1.4,1.3,1.2,1.1,1.05,1.0]
    val_loss = [2.6,2.2,1.9,1.7,1.5,1.4,1.3,1.2,1.15,1.1]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=epochs, y=train_loss, mode='lines+markers', name='Training Loss'))
    fig.add_trace(go.Scatter(x=epochs, y=val_loss, mode='lines+markers', name='Validation Loss'))
    fig.update_layout(title="Loss Over Epochs", xaxis_title="Epoch", yaxis_title="Loss", hovermode='x unified', height=400)
    st.plotly_chart(fig, use_container_width=True)

# ----------------- Training -----------------
elif page == "🎓 Training":
    st.markdown('<p class="main-header">Model Training</p>', unsafe_allow_html=True)
    st.info("Training simulation - on Termux we only mock training for now.")
    model_name = st.text_input("Model Name", placeholder="my-custom-model")
    if st.button("🚀 Start Training"):
        if model_name:
            st.session_state.models.append({
                'name': model_name, 'type': 'DistilGPT2', 'size':'82M', 'accuracy':'Training...',
                'date': datetime.now().strftime("%Y-%m-%d %H:%M"), 'status':'training'
            })
            st.session_state.training_history.append({
                'model': model_name, 'started': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'status':'running'
            })
            st.session_state.active_training = True
            st.success(f"✅ Training started for {model_name}")
        else:
            st.error("❌ Please provide a model name")

# ----------------- Models -----------------
elif page == "🔍 Models":
    st.markdown('<p class="main-header">Model Management</p>', unsafe_allow_html=True)
    if len(st.session_state.models) == 0:
        st.info("No models available. Start training to create one.")
    else:
        for model in st.session_state.models:
            st.markdown(f"### {model['name']}")
            st.caption(f"Type: {model['type']}")
            st.metric("Size", model['size'])
            st.metric("Accuracy", model['accuracy'])
            st.markdown("---")

# ----------------- Chat -----------------
elif page == "💬 Chat":
    st.markdown('<p class="main-header">MicroLLM Chat</p>', unsafe_allow_html=True)
    st.info("Chat with your model (CPU-light version). Upload documents to interact with them.")
    
    uploaded_file = st.file_uploader("Upload a document (.txt)", type=['txt'])
    if uploaded_file:
        text_data = uploaded_file.read().decode("utf-8")
        st.session_state.chat_history.append({"role":"system","content":text_data})
        st.success("📄 Document loaded successfully!")

    # Load DistilGPT2 pipeline
    @st.cache_resource
    def load_model():
        tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
        model = AutoModelForCausalLM.from_pretrained("distilgpt2")
        return pipeline("text-generation", model=model, tokenizer=tokenizer)

    generator = load_model()

    user_input = st.text_input("You:", key="user_input")
    if st.button("Send") and user_input:
        st.session_state.chat_history.append({"role":"user","content":user_input})
        # Prepare prompt from document + chat
        prompt = "\n".join([m["content"] for m in st.session_state.chat_history])
        result = generator(prompt, max_length=200, do_sample=True)[0]["generated_text"]
        st.session_state.chat_history.append({"role":"bot","content":result})
    
    # Display chat
    for message in st.session_state.chat_history[-10:]:
        role = "👤 You" if message["role"]=="user" else "🤖 MicroLLM"
        st.markdown(f"**{role}:** {message['content']}")

# ----------------- Footer -----------------
st.markdown("---")
st.markdown("<div style='text-align:center;color:#666;padding:20px;'>MicroLLM Studio v1.0 | CPU-light | No-Code Version</div>", unsafe_allow_html=True)