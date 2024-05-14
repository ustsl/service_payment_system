from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, field_validator

from src.settings import PaymentSystems, ServiceSystems

#########################
# BLOCK WITH API MODELS #
#########################


class InvoiceId(BaseModel):
    uuid: UUID


class InvoiceCreateBody(BaseModel):
    invoice_id: str
    user_id: str
    payment_system_name: PaymentSystems
    service_system_name: ServiceSystems
    amount: float

    @field_validator("amount")
    def amount_must_be_greater_than_one(cls, v):
        if v <= 1:
            raise ValueError("Amount must be greater than 1")
        return v


class InvoiceStatusBody(InvoiceId, InvoiceCreateBody):
    is_paid: bool
    time_create: datetime
