from fastapi import FastAPI
from api.routes import generate, auth

app = FastAPI(title="ARSLM API", version="1.0.0")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(generate.router, prefix="/generate", tags=["generate"])