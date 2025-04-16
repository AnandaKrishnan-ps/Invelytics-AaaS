from typing import Any, List

from app.core.logs import get_logs_service
from app.dependencies.inventory_deps import get_inventory_logs_service
from app.models.logs_schema import InventoryLogResponse
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.get("/", response_model=List[InventoryLogResponse])
async def get_logs(
    log_service: Any = Depends(get_inventory_logs_service),
    limit: int = 50,
    offset: int = 0,
    sort_by: str = "date",
    sort_order: str = "desc",
) -> List[InventoryLogResponse]:
    """
    Fetch all inventory change logs for a given item_id.

    Args:
        item_id: The unique identifier of the inventory item.
        log_service: A service to interact with the logs database (dependency injection).

    Returns:
        A list of log entries associated with the given item_id.
    """
    try:
        logs = await get_logs_service(
            log_service,
            limit,
            offset,
            sort_by,
            sort_order,
        )
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
