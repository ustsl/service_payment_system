from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.utils.oauth.api_verify_token import verify_admin_token

from .actions import _create_new_invoice, _show_invoices, _show_invoice
from .schemas import InvoiceCreateBody, InvoiceStatusBody

invoice_router = APIRouter(dependencies=[Depends(verify_admin_token)])


@invoice_router.post("/", response_model=InvoiceStatusBody)
async def create_user(body: InvoiceCreateBody, db: AsyncSession = Depends(get_db)):

    return await _create_new_invoice(body, db)


@invoice_router.get("/")
async def show_invoices(
    is_paid: bool | None = None, offset: int = 0, db: AsyncSession = Depends(get_db)
):
    return await _show_invoices(offset=offset, is_paid=is_paid, db=db)


@invoice_router.get("/{uuid}")
async def get_invoice(uuid: str, db: AsyncSession = Depends(get_db)):
    res = await _show_invoice(uuid, db)
    return res
