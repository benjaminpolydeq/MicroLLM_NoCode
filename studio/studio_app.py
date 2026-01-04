# MicroLLM Studio - Training & Management Dashboard
"""
MicroLLM Studio - Streamlit Dashboard
A complete interface for training and managing specialized language models
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time
import numpy as np

Page Configuration

st.set_page_config(
page_title="MicroLLM Studio",
page_icon="🤖",
layout="wide",
initial_sidebar_state="expanded"
)

Custom CSS

st.markdown("""

<style>  
    .main-header {  
        font-size: 3rem;  
        font-weight: bold;  
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);  
        -webkit-background-clip: text;  
        -webkit-text-fill-color: transparent;  
        margin-bottom: 0.5rem;  
    }  
    .metric-card {  
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);  
        padding: 20px;  
        border-radius: 10px;  
        color: white;  
        margin: 10px 0;  
    }  
    .status-badge {  
        padding: 5px 15px;  
        border-radius: 20px;  
        font-weight: bold;  
        display: inline-block;  
    }  
    .status-active {  
        background-color: #10b981;  
        color: white;  
    }  
    .status-idle {  
        background-color: #6b7280;  
        color: white;  
    }  
</style>  """, unsafe_allow_html=True)

Initialize Session State

if 'training_history' not in st.session_state:
st.session_state.training_history = []
if 'models' not in st.session_state:
st.session_state.models = []
if 'active_training' not in st.session_state:
st.session_state.active_training = False

Sidebar Navigation

with st.sidebar:
st.image("https://via.placeholder.com/200x80/667eea/ffffff?text=MicroLLM", width=200)
st.markdown("---")

page = st.radio(  
    "Navigation",  
    ["🏠 Dashboard", "🎓 Training", "🔍 Models", "📊 Analytics", "⚙️ Settings"],  
    label_visibility="collapsed",  
    key="main_navigation"  
)  
  
st.markdown("---")  
st.markdown("### System Status")  
system_status = "🟢 Active" if st.session_state.active_training else "⚪ Idle"  
st.markdown(f"**Status:** {system_status}")  
st.markdown(f"**Models:** {len(st.session_state.models)}")  
st.markdown(f"**Training Jobs:** {len(st.session_state.training_history)}")  
  
st.markdown("---")  
st.markdown("### Quick Actions")  
if st.button("🔄 Refresh Data", use_container_width=True, key="sidebar_refresh"):  
    st.success("Data refreshed!")  
    time.sleep(0.5)  
if st.button("📥 Export Report", use_container_width=True, key="sidebar_export"):  
    st.info("Export functionality coming soon!")

--- Main Content ---

Dashboard Page

if page == "🏠 Dashboard":
st.markdown('<p class="main-header">MicroLLM Studio Dashboard</p>', unsafe_allow_html=True)
st.markdown("Democratizing Proprietary AI - Train specialized language models on limited private data")

# Key Metrics  
col1, col2, col3, col4 = st.columns(4)  
  
col1.metric("Active Models", len(st.session_state.models), delta="+2 this week")  
col2.metric("Training Jobs", len(st.session_state.training_history), delta="3 completed")  
col3.metric("GPU Usage", "45%", delta="-5%")  
col4.metric("Avg. Accuracy", "87.3%", delta="+2.1%")  
  
st.markdown("---")  
  
# Recent Activity & System Overview  
col1, col2 = st.columns([2, 1])  
  
with col1:  
    st.subheader("📈 Training Progress")  
    epochs = list(range(1, 11))  
    train_loss = [2.5, 2.1, 1.8, 1.6, 1.4, 1.3, 1.2, 1.1, 1.05, 1.0]  
    val_loss = [2.6, 2.2, 1.9, 1.7, 1.5, 1.4, 1.3, 1.2, 1.15, 1.1]  
      
    fig = go.Figure()  
    fig.add_trace(go.Scatter(x=epochs, y=train_loss, mode='lines+markers', name='Training Loss', line=dict(color='#667eea', width=3)))  
    fig.add_trace(go.Scatter(x=epochs, y=val_loss, mode='lines+markers', name='Validation Loss', line=dict(color='#764ba2', width=3)))  
    fig.update_layout(title="Loss Over Epochs", xaxis_title="Epoch", yaxis_title="Loss", hovermode='x unified', height=400)  
    st.plotly_chart(fig, use_container_width=True)  
  
with col2:  
    st.subheader("🎯 Quick Stats")  
    st.markdown("""  
    <div class="metric-card">  
        <h4 style="margin-top:0;">ARSLM Core</h4>  
        <p style="margin-bottom:0;">✅ Efficiency: 95%</p>  
        <p style="margin-bottom:0;">✅ Explainability: High</p>  
        <p style="margin-bottom:0;">✅ Security: Enterprise</p>  
    </div>  
    """, unsafe_allow_html=True)  
    st.markdown("### Resource Usage")  
    st.progress(0.45, text="GPU: 45%")  
    st.progress(0.62, text="CPU: 62%")  
    st.progress(0.38, text="Memory: 38%")  
    st.progress(0.71, text="Storage: 71%")  
  
st.markdown("---")  
st.subheader("🤖 Recent Models")  
if len(st.session_state.models) == 0:  
    st.info("No models trained yet. Start by creating a new training job!")  
else:  
    for i, model in enumerate(st.session_state.models[-3:]):  
        with st.expander(f"📦 {model['name']}", expanded=False):  
            st.write(f"**Type:** {model['type']}")  
            st.write(f"**Size:** {model['size']}")  
            st.write(f"**Accuracy:** {model['accuracy']}")  
            st.write(f"**Created:** {model['date']}")  
            st.button("🚀 Deploy", key=f"dashboard_deploy_{model['name']}_{i}")  
            st.button("📊 Details", key=f"dashboard_details_{model['name']}_{i}")

Training Page

elif page == "🎓 Training":
st.markdown('<p class="main-header">Model Training</p>', unsafe_allow_html=True)
tabs = st.tabs(["New Training", "Training Queue", "History"])

with tabs[0]:  
    st.subheader("Create New Training Job")  
    col1, col2 = st.columns(2)  
    with col1:  
        model_name = st.text_input("Model Name", placeholder="my-custom-model", key="training_model_name")  
        model_type = st.selectbox("Model Architecture", ["ARSLM-Micro (100M)", "ARSLM-Small (300M)", "ARSLM-Medium (1B)", "ARSLM-Large (3B)"], key="training_model_type")  
        dataset_source = st.selectbox("Data Source", ["Upload Files", "S3 Bucket", "Local Directory", "Database"], key="dataset_source")  
    with col2:  
        training_mode = st.selectbox("Training Mode", ["Fine-tuning", "From Scratch", "Transfer Learning"], key="training_mode")  
        batch_size = st.slider("Batch Size", 8, 128, 32, key="batch_size")  
        learning_rate = st.number_input("Learning Rate", min_value=0.00001, max_value=0.01, value=0.001, format="%.5f", key="learning_rate")  
      
    st.markdown("### Advanced Settings")  
    col1, col2, col3 = st.columns(3)  
    with col1:  
        epochs = st.number_input("Epochs", 1, 100, 10, key="epochs")  
        warmup_steps = st.number_input("Warmup Steps", 0, 1000, 100, key="warmup_steps")  
    with col2:  
        max_seq_length = st.number_input("Max Sequence Length", 128, 2048, 512, key="max_seq_length")  
        gradient_acc = st.number_input("Gradient Accumulation", 1, 16, 4, key="gradient_acc")  
    with col3:  
        weight_decay = st.number_input("Weight Decay", 0.0, 0.1, 0.01, format="%.3f", key="weight_decay")  
        dropout = st.slider("Dropout", 0.0, 0.5, 0.1, key="dropout")  
      
    uploaded_file = st.file_uploader("Upload Training Data", type=['txt', 'json', 'jsonl', 'csv'], key="uploaded_file")  
    validation_split = st.slider("Validation Split (%)", 0, 30, 10, key="validation_split")  
      
    col1, col2 = st.columns(2)  
    with col1:  
        enable_encryption = st.checkbox("Enable Data Encryption", value=True, key="enable_encryption")  
        enable_audit = st.checkbox("Enable Audit Logging", value=True, key="enable_audit")  
    with col2:  
        enable_privacy = st.checkbox("Enable Differential Privacy", value=False, key="enable_privacy")  
        enable_federated = st.checkbox("Federated Learning Mode", value=False, key="enable_federated")  
      
    col1, col2, col3 = st.columns([1, 1, 2])  
    with col1:  
        if st.button("🚀 Start Training", key="start_training_btn"):  
            if model_name:  
                new_model = {  
                    'name': model_name,  
                    'type': model_type,  
                    'size': model_type.split('(')[1].strip(')'),  
                    'accuracy': 'Training...',  
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M"),  
                    'status': 'training'  
                }  
                st.session_state.models.append(new_model)  
                st.session_state.training_history.append({  
                    'model': model_name,  
                    'started': datetime.now().strftime("%Y-%m-%d %H:%M"),  
                    'status': 'running'  
                })  
                st.session_state.active_training = True  
                st.success(f"✅ Training started for {model_name}!")  
            else:  
                st.error("❌ Please provide a model name")  
    with col2:  
        if st.button("💾 Save Configuration", key="save_config_btn"):  
            st.info("💾 Configuration saved!")  
    with col3:  
        st.markdown("💡 **Tip:** Start with ARSLM-Micro for quick experiments")  
  
with tabs[1]:  
    st.subheader("Training Queue")  
    progress_container = st.container()  
    with progress_container:  
        progress_bar = st.progress(0, key="training_progress_bar")  
        status_text = st.empty()  
        if st.session_state.active_training:  
            import random  
            progress = random.randint(15, 85)  
            progress_bar.progress(progress)  
            status_text.text(f"Training in progress... {progress}%")  
        else:  
            st.info("No active training jobs")  
  
with tabs[2]:  
    st.subheader("Training History")  
    if len(st.session_state.training_history) == 0:  
        st.info("No training history available")  
    else:  
        df = pd.DataFrame(st.session_state.training_history)  
        st.dataframe(df, use_container_width=True)

Models Page

elif page == "🔍 Models":
st.markdown('<p class="main-header">Model Management</p>', unsafe_allow_html=True)
if len(st.session_state.models) == 0:
st.info("No models available. Create your first model in the Training section!")
else:
for i, model in enumerate(st.session_state.models):
with st.container():
st.markdown(f"### {model['name']}")
st.caption(f"Type: {model['type']}")
st.metric("Size", model['size'])
st.metric("Accuracy", model['accuracy'])
st.button("🚀 Deploy", key=f"models_deploy_{model['name']}{i}")
st.button("🗑️ Delete", key=f"models_delete{model['name']}_{i}")
st.markdown("---")

Analytics and Settings remain unchanged (add keys if necessary)

Footer

st.markdown("---")
st.markdown("""

<div style='text-align: center; color: #666; padding: 20px;'>  
    <p>MicroLLM Studio v1.0 | Built on ARSLM Framework</p>  
    <p>Democratizing Proprietary AI for Enterprise & Regulated Environments</p>  
</div>  
""", unsafe_allow_html=True)  