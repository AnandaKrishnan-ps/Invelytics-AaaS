from app.api.inventory import router as inventory_router
from app.api.recommendations import router as recommendations_router
from app.api.surplus import router as surplus_router
from app.api.logs import router as logs_router

__all__ = [
    "inventory_router",
    "recommendations_router",
    "surplus_router",
    "logs_router",
]
