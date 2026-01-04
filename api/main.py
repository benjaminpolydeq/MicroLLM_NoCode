from fastapi import FastAPI
from api.routes import auth, generate

app = FastAPI(title="ARSLM MicroLLM API")
app.include_router(auth.router)
app.include_router(generate.router)