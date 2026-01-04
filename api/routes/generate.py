from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from core.base_model.arslm.model import ARSLMModel

router = APIRouter()

# Load model once (ARSLM real)
model = ARSLMModel(model_path="gpt2", device="cpu")  # change path for your ARSLM weights

class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 256
    temperature: float = 0.7

@router.post("/generate")
def generate(request: GenerateRequest, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    # Call ARSLM real model
    output = model.generate(request.prompt, max_tokens=request.max_tokens, temperature=request.temperature)
    return {"output": output}