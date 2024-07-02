import jwt
import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.adapter import model_to_dict
from src.db.invoice.dals import InvoiceDAL
from src.db.invoice.models import InvoiceModel
from src.utils.wrappers.handle import handle_dal_errors
from src.utils.invoice_processing.handler import get_api_request_data_for_change_balance

from .schemas import InvoiceResultStatus


@handle_dal_errors
async def _invoice_confirmation(
    uuid: str, token: str, db: AsyncSession
) -> InvoiceResultStatus:
    async with db as session:
        async with session.begin():
            message = "problem"
            obj_dal = InvoiceDAL(session, InvoiceModel)
            result = await obj_dal.get(uuid=uuid)
            result_dict = model_to_dict(result)

            if result_dict.get("status") == 404:
                return InvoiceResultStatus(status=False, message="Invoice not found")

            if not result:
                return InvoiceResultStatus(status=False, message="Invoice not found")

            if result.is_paid:
                return InvoiceResultStatus(status=False, message="Invoice already paid")

            # if not await _is_token_valid(token, result):
            #     return InvoiceResultStatus(status=False, message="Invalid token")

            if not await _change_balance(result):
                return InvoiceResultStatus(
                    status=False, message="Failed to change balance"
                )

            await obj_dal.update(uuid=uuid, is_paid=True)
            message = "It's ok"

            return InvoiceResultStatus(status=True, message=message)


async def _is_token_valid(token: str, result: InvoiceModel) -> bool:
    service = result.service_system_name.name.lower()
    data = get_api_request_data_for_change_balance(
        service_name=service,
        acc_id=result.user_id,
        balance=float(result.amount),
    )

    key_token = data.get("token")
    try:
        decoded_token = jwt.decode(token, key_token, algorithms=["HS256"])
        token_id = decoded_token.get("id", "undefined")
        return token_id == result.uuid
    except:
        False


async def _change_balance(result: InvoiceModel) -> bool:
    service = result.service_system_name.name.lower()

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

    if response.status_code == 200:
        return True
    return False
