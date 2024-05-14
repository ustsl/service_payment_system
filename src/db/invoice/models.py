from sqlalchemy import Column, String, Boolean, Numeric, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
import uuid

from src.db.models import TimeModel
from src.settings import PaymentSystems, ServiceSystems


class InvoiceModel(TimeModel):
    __tablename__ = "invoice"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    invoice_id = Column(String, nullable=False, unique=True)
    user_id = Column(String, nullable=False)
    payment_system_name = Column(Enum(PaymentSystems), nullable=False)
    service_system_name = Column(Enum(ServiceSystems), nullable=False)
    is_paid = Column(Boolean, default=True, nullable=True)
    amount = Column(Numeric(10, 2), nullable=False, default=0.00)

    @validates("payment_system_name")
    def validate_payment_system_name(self, key, payment_system_name):
        if payment_system_name not in PaymentSystems.__members__.values():
            raise ValueError(
                f"Payment system {payment_system_name} is not a valid choice"
            )
        return payment_system_name

    @validates("service_system_name")
    def validate_service_system_name(self, key, service_system_name):
        if service_system_name not in ServiceSystems.__members__.values():
            raise ValueError(
                f"Service system {service_system_name} is not a valid choice"
            )
        return service_system_name
