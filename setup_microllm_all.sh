#!/bin/bash

echo "✅ Début de la création MicroLLM SaaS Phase 1+2"

# ----------------------
# Création dossiers
# ----------------------
mkdir -p backend/app/{core,api,security,models,schemas,services,tests}
mkdir -p frontend

# ----------------------
# Création fichiers backend
# ----------------------
touch backend/app/main.py
touch backend/app/core/config.py
touch backend/app/security/api_key.py
touch backend/app/api/health.py
touch backend/requirements.txt
touch backend/Dockerfile

# ----------------------
# Création fichiers frontend
# ----------------------
touch frontend/app.py
touch frontend/requirements.txt
touch frontend/Dockerfile

# ----------------------
# Fichiers généraux
# ----------------------
touch docker-compose.yml
touch .env.example
touch .gitignore
touch .dockerignore
touch Makefile

# ----------------------
# Contenu backend FastAPI minimal
# ----------------------
cat > backend/app/main.py <<EOL
from fastapi import FastAPI
from app.api.health import router as health_router

app = FastAPI(title="MicroLLM SaaS")
app.include_router(health_router)
EOL

cat > backend/app/core/config.py <<EOL
import os

API_KEY = os.getenv("MICROLLM_API_KEY", "dev-secret-key")
PROJECT_NAME = "MicroLLM SaaS"
ENV = os.getenv("ENV", "development")
EOL

cat > backend/app/security/api_key.py <<EOL
from fastapi import Header, HTTPException

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != "dev-secret-key":
        raise HTTPException(status_code=401, detail="Invalid API Key")
EOL

cat > backend/app/api/health.py <<EOL
from fastapi import APIRouter, Depends
from app.security.api_key import verify_api_key

router = APIRouter()

@router.get("/health")
def health_check(api_key: str = Depends(verify_api_key)):
    return {"status": "ok", "service": "MicroLLM backend"}
EOL

cat > backend/requirements.txt <<EOL
fastapi
uvicorn
python-dotenv
EOL

# ----------------------
# Contenu frontend Streamlit minimal
# ----------------------
cat > frontend/app.py <<EOL
import streamlit as st
import requests

st.set_page_config(page_title="MicroLLM Studio", layout="wide")
st.title("MicroLLM Studio - Frontend MVP")

API_KEY = st.text_input("Enter your API Key", "")
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
EOL

cat > frontend/requirements.txt <<EOL
streamlit
requests
EOL

# ----------------------
# Contenu fichiers généraux
# ----------------------
cat > .gitignore <<EOL
__pycache__/
*.pyc
.env
.env.local
EOL

cat > .dockerignore <<EOL
__pycache__/
*.pyc
.env
.git
EOL

cat > docker-compose.yml <<EOL
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
EOL

cat > Makefile <<EOL
.PHONY: up
up:
\tdocker-compose up --build
EOL

echo "✅ MicroLLM SaaS Phase 1+2 créé avec backend FastAPI et frontend Streamlit"
echo "📌 Prochaine étape : git add . && git commit -m 'feat: initial MicroLLM structure' && git push"
