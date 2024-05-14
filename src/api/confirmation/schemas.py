from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, field_validator

from src.settings import PaymentSystems, ServiceSystems

#########################
# BLOCK WITH API MODELS #
#########################


class InvoiceConfirmation(BaseModel):
    invoice_id: str
    token: str


class InvoiceResultStatus(BaseModel):
    status: bool
    message: str
