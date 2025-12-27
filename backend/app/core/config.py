import os

API_KEY = os.getenv("MICROLLM_API_KEY", "dev-secret-key")
PROJECT_NAME = "MicroLLM SaaS"
ENV = os.getenv("ENV", "development")
