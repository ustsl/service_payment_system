from fastapi import HTTPException

from src.db.adapter import model_to_dict
from src.db.invoice.dals import InvoiceDAL
from src.db.invoice.models import InvoiceModel
from src.utils.wrappers.handle import handle_dal_errors

from .schemas import InvoiceCreateBody, InvoiceStatusBody


@handle_dal_errors
async def _create_new_invoice(body: InvoiceCreateBody, db) -> InvoiceStatusBody:
    async with db as session:
        async with session.begin():
            data_to_create = body.model_dump()
            obj_dal = InvoiceDAL(session, InvoiceModel)
            result = await obj_dal.create(**data_to_create)
            if isinstance(result, dict) and result.get("error"):
                raise HTTPException(status_code=500, detail=result["error"])
            result_dict = model_to_dict(result)
            return InvoiceStatusBody(**result_dict)
