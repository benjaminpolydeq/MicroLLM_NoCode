import streamlit as st
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8000"
ACCESS_TOKEN = ""

st.set_page_config(page_title="MicroLLM Studio", page_icon="🤖", layout="wide")

if 'models' not in st.session_state:
    st.session_state.models = []
if 'training_history' not in st.session_state:
    st.session_state.training_history = []
if 'active_training' not in st.session_state:
    st.session_state.active_training = False

def login(username: str):
    global ACCESS_TOKEN
    response = requests.post(f"{API_URL}/auth/login", json={"username": username})
    if response.status_code == 200:
        ACCESS_TOKEN = response.json()["access_token"]
        st.success(f"Logged in as {username}")
    else:
        st.error("Login failed")

def generate(prompt: str, max_tokens: int = 256, temperature: float = 0.7):
    if not ACCESS_TOKEN:
        st.warning("Login first")
        return ""
    headers = {"Authorization": ACCESS_TOKEN}
    payload = {"prompt": prompt, "max_tokens": max_tokens, "temperature": temperature}
    response = requests.post(f"{API_URL}/generate", headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["output"]
    st.error("Failed to generate")
    return ""

def start_training(model_name: str, model_type: str):
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
    st.success(f"Training started for {model_name}!")

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/667eea/ffffff?text=MicroLLM", width=200)
    st.markdown("---")
    username = st.text_input("Username")
    if st.button("Login"):
        login(username)
    max_tokens = st.slider("Max Tokens", 32, 1024, 256)
    temperature = st.slider("Temperature", 0.1, 1.0, 0.7)
    status = "🟢 Active" if st.session_state.active_training else "⚪ Idle"
    st.markdown(f"**Status:** {status}")

# Tabs
tabs = st.tabs(["🏠 Dashboard", "📝 No-Code", "🎓 Training", "📊 Analytics"])

with tabs[0]:
    st.subheader("Dashboard")
    st.write(st.session_state.models[-3:])

with tabs[1]:
    st.subheader("No-Code Interface")
    prompt = st.text_area("Enter prompt:")
    if st.button("Generate"):
        if prompt.strip():
            output = generate(prompt, max_tokens=max_tokens, temperature=temperature)
            st.text(output)

with tabs[2]:
    st.subheader("Create Training Job")
    model_name = st.text_input("Model Name")
    model_type = st.selectbox("Model Type", ["ARSLM-Micro", "ARSLM-Small", "ARSLM-Medium", "ARSLM-Large"])
    if st.button("Start Training"):
        if model_name.strip():
            start_training(model_name, model_type)

with tabs[3]:
    st.subheader("Training Analytics")
    st.dataframe(st.session_state.training_history)