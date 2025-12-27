#!/bin/bash
echo "Création dossiers backend/frontend..."
mkdir -p backend/app/{core,api,security,models,schemas,services,tests}
mkdir -p frontend

echo "Création fichiers principaux..."
touch backend/app/main.py
touch backend/app/core/config.py
touch backend/app/security/api_key.py
touch backend/app/api/health.py
touch backend/requirements.txt
touch backend/Dockerfile
touch frontend/requirements.txt
touch frontend/Dockerfile
touch docker-compose.yml
touch .env.example
touch .dockerignore
touch .gitignore
touch Makefile

echo "Écriture contenu FastAPI minimal..."
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

cat > frontend/requirements.txt <<EOL
streamlit
requests
EOL

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

echo "✅ Structure MicroLLM SaaS Phase 1+2 créée avec code FastAPI minimal!"
