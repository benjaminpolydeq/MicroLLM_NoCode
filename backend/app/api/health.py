from fastapi import APIRouter, Depends
from app.security.api_key import verify_api_key

router = APIRouter()

@router.get("/health")
def health_check(api_key: str = Depends(verify_api_key)):
    return {"status": "ok", "service": "MicroLLM backend"}
