from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db

from .actions import _invoice_confirmation
from .schemas import InvoiceConfirmation, InvoiceResultStatus

confirmation_router = APIRouter()


@confirmation_router.post("/", response_model=InvoiceResultStatus)
async def invoice_confirmation(
    body: InvoiceConfirmation, db: AsyncSession = Depends(get_db)
):
    return await _invoice_confirmation(uuid=body.invoice_id, db=db)
