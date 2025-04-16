from app.dependencies.inventory_deps import get_inventory_service
from app.dependencies.logistics_deps import get_logistics_service
from app.dependencies.surplus_deps import get_surplus_service

__all__ = ["get_inventory_service", "get_surplus_service", "get_logistics_service"]
