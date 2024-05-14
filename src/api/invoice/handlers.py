import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from .schemas import InvoiceCreateBody, InvoiceStatusBody
from src.db.session import get_db
from src.utils.oauth.api_verify_token import verify_token
from .actions import _create_new_invoice


invoice_router = APIRouter(dependencies=[Depends(verify_token)])


@invoice_router.post("/", response_model=InvoiceStatusBody)
async def create_user(body: InvoiceCreateBody, db: AsyncSession = Depends(get_db)):

    return await _create_new_invoice(body, db)


# @user_router.get("/")
# async def get_users(db: AsyncSession = Depends(get_db)):
#     return await _get_users(db)


# @user_router.get("/{telegram_id}", response_model=UserDataExtend)
# async def get_user(telegram_id: str, db: AsyncSession = Depends(get_db)):
#     res = await _get_user(telegram_id, db)
#     return res


# @user_router.put("/{telegram_id}/balance")
# async def set_user_balance(
#     telegram_id: str, balance: UserBalance, db: AsyncSession = Depends(get_db)
# ):
#     res = await _update_user_account_balance(telegram_id, balance, db)
#     return res


# @user_router.put("/{telegram_id}/prompt")
# async def set_user_prompt(
#     telegram_id: str, updates: dict, db: AsyncSession = Depends(get_db)
# ):
#     # This function may changes user preset prompt, its need for telegram part of app
#     res = await _update_user_settings_prompt(
#         telegram_id=telegram_id, prompt_id=updates.get("prompt_id"), db=db
#     )
#     return res


# @user_router.put("/{telegram_id}/block")
# async def set_block_user(
#     telegram_id: str, updates: dict, db: AsyncSession = Depends(get_db)
# ):
#     res = await _block_user(
#         telegram_id=telegram_id, is_active=updates.get("is_active"), db=db
#     )
#     return res
