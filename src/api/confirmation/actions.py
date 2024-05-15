import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.adapter import model_to_dict
from src.db.invoice.dals import InvoiceDAL
from src.db.invoice.models import InvoiceModel
from src.utils.wrappers.handle import handle_dal_errors
from src.utils.invoice_processing.handler import get_api_request_data_for_change_balance

from .schemas import InvoiceResultStatus


@handle_dal_errors
async def _invoice_confirmation(uuid: str, db: AsyncSession) -> InvoiceResultStatus:
    async with db as session:
        async with session.begin():
            message = "problem"
            obj_dal = InvoiceDAL(session, InvoiceModel)
            result = await obj_dal.get(uuid=uuid)
            try:
                result_dict = model_to_dict(result)
                if result_dict.get("uuid"):
                    if result.is_paid != True:
                        await obj_dal.update(uuid=uuid, is_paid=True)
                        service = (result.service_system_name.name).lower()
                        data = get_api_request_data_for_change_balance(
                            service_name=service,
                            acc_id=result.user_id,
                            balance=float(result.amount),
                        )
                        async with httpx.AsyncClient() as client:
                            response = await client.put(
                                url=data.get("url"),
                                headers=data.get("headers"),
                                json=data.get("body"),
                            )
                            response.raise_for_status()
                        message = "It's ok"
                print("finish")
            except Exception as e:
                print(e)
                print(12323)
                pass

            return InvoiceResultStatus(status=True, message=message)
