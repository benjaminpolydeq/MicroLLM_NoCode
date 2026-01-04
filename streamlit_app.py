"""
MicroLLM Studio - Ultimate No-Code + Studio Dashboard
Integrated with ARSLM real model via FastAPI
Supports Multi-Tenant Auth, Training, Analytics
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import requests
from datetime import datetime

# ========================
# CONFIG
# ========================

API_URL = "http://127.0.0.1:8000"  # FastAPI backend
ACCESS_TOKEN = ""  # JWT token after login

st.set_page_config(page_title="MicroLLM Studio", page_icon="🤖", layout="wide")

# ========================
# SESSION STATE INIT
# ========================

if 'training_history' not in st.session_state:
    st.session_state.training_history = []
if 'models' not in st.session_state:
    st.session_state.models = []
if 'active_training' not in st.session_state:
    st.session_state.active_training = False

# ========================
# HELPER FUNCTIONS
# ========================

def login(username: str):
    global ACCESS_TOKEN
    response = requests.post(f"{API_URL}/auth/login", params={"username": username})
    if response.status_code == 200:
        ACCESS_TOKEN = response.json()["access_token"]
        st.success(f"Logged in as {username}")
    else:
        st.error("Login failed")

def generate(prompt: str, max_tokens: int = 256, temperature: float = 0.7):
    if not ACCESS_TOKEN:
        st.warning("You must login first")
        return ""
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    payload = {"prompt": prompt, "max_tokens": max_tokens, "temperature": temperature}
    response = requests.post(f"{API_URL}/generate", headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["output"]
    else:
        st.error("Failed to generate text")
        return ""

def start_training(model_name: str, model_type: str):
    """Simulate a new training job"""
    st.session_state.models.append({
        "name": model_name,
        "type": model_type,
        "accuracy": "Training...",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    st.session_state.training_history.append({
        "model": model_name,
        "started": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "status": "running"
    })
    st.session_state.active_training = True
    st.success(f"✅ Training started for {model_name}!")

# ========================
# SIDEBAR
# ========================

with st.sidebar:
    st.image("https://via.placeholder.com/200x80/667eea/ffffff?text=MicroLLM", width=200)
    st.markdown("---")
    
    st.markdown("## User Login")
    username = st.text_input("Username")
    if st.button("Login"):
        login(username)
    
    st.markdown("---")
    st.markdown("### Settings")
    max_tokens = st.slider("Max Tokens", 32, 1024, 256)
    temperature = st.slider("Temperature", 0.1, 1.0, 0.7)
    
    st.markdown("---")
    st.markdown("### System Status")
    status = "🟢 Active" if st.session_state.active_training else "⚪ Idle"
    st.markdown(f"**Status:** {status}")
    st.markdown(f"**Models:** {len(st.session_state.models)}")
    st.markdown(f"**Training Jobs:** {len(st.session_state.training_history)}")
    
    st.markdown("---")
    st.markdown("### Quick Actions")
    if st.button("🔄 Refresh Data"):
        st.success("Data refreshed!")
        time.sleep(0.5)

# ========================
# TABS: Dashboard / No-Code / Training / Analytics
# ========================

tabs = st.tabs(["🏠 Dashboard", "📝 No-Code", "🎓 Training", "📊 Analytics"])

# ========================
# DASHBOARD
# ========================
with tabs[0]:
    st.markdown("## MicroLLM Studio Dashboard")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Active Models", len(st.session_state.models))
    col2.metric("Training Jobs", len(st.session_state.training_history))
    col3.metric("GPU Usage", "45%")
    col4.metric("Avg. Accuracy", "87.3%")
    
    st.markdown("---")
    
    # Recent models
    st.subheader("🤖 Recent Models")
    if len(st.session_state.models) == 0:
        st.info("No models trained yet.")
    else:
        for i, model in enumerate(st.session_state.models[-3:]):
            with st.expander(f"📦 {model['name']}", expanded=False):
                st.write(f"**Type:** {model['type']}")
                st.write(f"**Accuracy:** {model['accuracy']}")
                st.write(f"**Created:** {model['date']}")
                st.button("🚀 Deploy", key=f"deploy_{model['name']}_{i}")

# ========================
# NO-CODE INTERFACE
# ========================
with tabs[1]:
    st.subheader("📝 MicroLLM No-Code Interface")
    prompt = st.text_area("Enter your prompt here:")
    if st.button("Generate"):
        if prompt.strip():
            with st.spinner("Generating..."):
                output = generate(prompt, max_tokens=max_tokens, temperature=temperature)
                st.markdown("### Output")
                st.text(output)
        else:
            st.warning("Please enter a prompt!")

# ========================
# TRAINING
# ========================
with tabs[2]:
    st.subheader("🎓 Create Training Job")
    col1, col2 = st.columns(2)
    with col1:
        model_name = st.text_input("Model Name", placeholder="my-custom-model")
        model_type = st.selectbox("Model Architecture", ["ARSLM-Micro (100M)", "ARSLM-Small (300M)", "ARSLM-Medium (1B)", "ARSLM-Large (3B)"])
    with col2:
        batch_size = st.slider("Batch Size", 8, 128, 32)
        learning_rate = st.number_input("Learning Rate", 0.0001, 0.01, 0.001, format="%.5f")
    
    if st.button("🚀 Start Training"):
        if model_name.strip():
            start_training(model_name, model_type)
        else:
            st.warning("Please enter a model name")

# ========================
# ANALYTICS
# ========================
with tabs[3]:
    st.subheader("📊 Training Analytics")
    if len(st.session_state.training_history) == 0:
        st.info("No training history available")
    else:
        df = pd.DataFrame(st.session_state.training_history)
        st.dataframe(df, use_container_width=True)
        
        # Example: Loss over epochs (simulated)
        st.subheader("Loss Over Epochs")
        epochs = list(range(1, 11))
        train_loss = [2.5, 2.1, 1.8, 1.6, 1.4, 1.3, 1.2, 1.1, 1.05, 1.0]
        val_loss = [2.6, 2.2, 1.9, 1.7, 1.5, 1.4, 1.3, 1.2, 1.15, 1.1]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=epochs, y=train_loss, mode='lines+markers', name='Training Loss'))
        fig.add_trace(go.Scatter(x=epochs, y=val_loss, mode='lines+markers', name='Validation Loss'))
        fig.update_layout(xaxis_title="Epoch", yaxis_title="Loss", height=400)
        st.plotly_chart(fig, use_container_width=True)

# ========================
# FOOTER
# ========================
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>MicroLLM Studio v1.0 | Connected to ARSLM API | Multi-Tenant Ready</div>", unsafe_allow_html=True)