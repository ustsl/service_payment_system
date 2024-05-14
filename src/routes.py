from fastapi.routing import APIRouter

from src.api.invoice.handlers import invoice_router
from src.api.confirmation.handlers import confirmation_router

# create the instance for the routes
main_api_router = APIRouter()

# set routes to the app instance
main_api_router.include_router(invoice_router, prefix="/v1/invoice", tags=["invoice"])
main_api_router.include_router(
    confirmation_router, prefix="/v1/confirm", tags=["confirm"]
)
