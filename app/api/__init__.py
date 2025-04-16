from app.api.inventory import router as inventory_router
from app.api.logistics import router as logistics_router
from app.api.recommendations import router as recommendations_router
from app.api.surplus import router as surplus_router

__all__ = [
    "inventory_router",
    "logistics_router",
    "recommendations_router",
    "surplus_router",
]