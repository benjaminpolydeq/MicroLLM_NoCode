from fastapi import Header, HTTPException

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != "dev-secret-key":
        raise HTTPException(status_code=401, detail="Invalid API Key")
