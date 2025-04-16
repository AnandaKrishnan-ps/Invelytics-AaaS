# api/inventory.py

from typing import Any, List

from app.core.inventory_logic import (
    add_inventory_item,
    get_all_inventory_items,
    update_inventory_item,
)
from app.dependencies.inventory_deps import (
    get_inventory_logs_service,
    get_inventory_service,
)
from app.models.inventory_schema import (
    InventoryItem,
    InventoryResponse,
    InventoryUpdate,
)
from fastapi import APIRouter, Depends, HTTPException, Query

router = APIRouter()


@router.get("/", response_model=List[InventoryResponse])
async def list_inventory(
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    service: Any = Depends(get_inventory_service),
    sort_by: str = Query("last_updated", regex="^(last_updated|name)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
) -> List[InventoryResponse]:
    try:

        return await get_all_inventory_items(
            service, limit=limit, skip=skip, sort_by=sort_by, sort_order=sort_order
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=InventoryResponse)
async def create_inventory_item(
    item: InventoryItem, service: Any = Depends(get_inventory_service)
) -> InventoryResponse:
    try:
        return await add_inventory_item(item, service)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{item_id}", response_model=InventoryResponse)
async def update_inventory(
    item_id: str,
    update: InventoryUpdate,
    service: Any = Depends(get_inventory_service),
    log_service: Any = Depends(get_inventory_logs_service),
) -> InventoryResponse:
    try:
        return await update_inventory_item(item_id, update, service, log_service)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
