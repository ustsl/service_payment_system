from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.adapter import model_to_dict
from src.db.invoice.dals import InvoiceDAL
from src.db.invoice.models import InvoiceModel
from src.utils.wrappers.handle import handle_dal_errors

from .schemas import InvoiceCreateBody, InvoiceList, InvoiceStatusBody


@handle_dal_errors
async def _create_new_invoice(
    body: InvoiceCreateBody, db: AsyncSession
) -> InvoiceStatusBody:
    async with db as session:
        async with session.begin():
            data_to_create = body.model_dump()
            obj_dal = InvoiceDAL(session, InvoiceModel)
            result = await obj_dal.create(**data_to_create)
            if isinstance(result, dict) and result.get("error"):
                raise HTTPException(status_code=500, detail=result["error"])
            result_dict = model_to_dict(result)
            return InvoiceStatusBody(**result_dict)


@handle_dal_errors
async def _show_invoices(
    db: AsyncSession,
    is_paid: bool | None = None,
    offset: int = 0,
) -> InvoiceList:
    filters = {}
    if type(is_paid) is bool:
        print("bool")
        filters["is_paid"] = is_paid
    obj_dal = InvoiceDAL(db, InvoiceModel)
    results = await obj_dal.list(offset=offset, filters=filters)
    return results


@handle_dal_errors
async def _show_invoice(uuid: str, db: AsyncSession) -> InvoiceStatusBody:
    obj_dal = InvoiceDAL(db, InvoiceModel)
    result = await obj_dal.get(uuid=uuid)
    result_dict = model_to_dict(result)
    return InvoiceStatusBody(**result_dict)
