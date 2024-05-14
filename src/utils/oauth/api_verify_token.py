from fastapi import HTTPException
from fastapi import Request, HTTPException, status

from src.settings import SERVICE_TOKEN


async def verify_token(request: Request):
    token = request.headers.get("Authorization")
    if token != SERVICE_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token"
        )
