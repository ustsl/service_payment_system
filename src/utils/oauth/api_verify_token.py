from fastapi import HTTPException, Request, status

from src.settings import SERVICE_TOKEN


async def verify_admin_token(request: Request):
    token = request.headers.get("Authorization")
    if token != SERVICE_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token"
        )


# async def verify_payment_token(request: Request):
#     print(request)
#     print(3234234)
# token = request.data.get("token")
# if token != SERVICE_TOKEN:
#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token"
#     )
