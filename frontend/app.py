import streamlit as st
import requests
import os

st.set_page_config(page_title="MicroLLM Studio", layout="wide")
st.title("MicroLLM Studio - Frontend MVP")

# Clé API
API_KEY = st.text_input("Enter your API Key", "")

# URL backend
BACKEND_URL = st.text_input("Backend URL", "http://127.0.0.1:8000")

if st.button("Check Backend Health"):
    if not API_KEY:
        st.error("Please enter API Key")
    else:
        try:
            headers = {"x-api-key": API_KEY}
            response = requests.get(f"{BACKEND_URL}/health", headers=headers)
            if response.status_code == 200:
                st.success(response.json())
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"Connection failed: {e}")
