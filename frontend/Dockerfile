FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
Commit : feat: add frontend Dockerfile
📄 Fichier 10 : frontend/requirements.txt
Create new file : frontend/requirements.txt
Contenu :
streamlit==1.31.0
requests==2.31.0
python-dotenv==1.0.0
pandas==2.1.4
plotly==5.18.0
