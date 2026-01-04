from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    username: str

# In-memory token store (simulate multi-tenant)
TOKENS = {}

@router.post("/auth/login")
def login(data: LoginRequest):
    token = f"{data.username}-token"
    TOKENS[token] = data.username
    return {"access_token": token}