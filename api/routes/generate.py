from fastapi import APIRouter, Depends
from pydantic import BaseModel
from core.engine.arslm_engine import generate_text
from api.routes.auth import get_current_user

router = APIRouter()

class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 256
    temperature: float = 0.7

@router.post("/")
def generate(data: GenerateRequest, user=Depends(get_current_user)):
    output = generate_text(prompt=data.prompt, max_tokens=data.max_tokens, temperature=data.temperature)
    return {"tenant_id": user["tenant_id"], "output": output}