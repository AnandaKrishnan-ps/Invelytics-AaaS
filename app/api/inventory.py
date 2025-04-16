# api/inventory.py

from typing import List

from app.core.inventory_logic import (
    add_inventory_item,
    get_all_inventory_items,
    update_inventory_item,
)
from app.dependencies.inventory_deps import get_inventory_service
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
    service=Depends(get_inventory_service),
    ignore_limit: bool = Query(False),
):
    try:

        return await get_all_inventory_items(
            service, limit=limit, skip=skip, ignore_limit=ignore_limit
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=InventoryResponse)
async def create_inventory_item(
    item: InventoryItem, service=Depends(get_inventory_service)
):
    try:
        return await add_inventory_item(item, service)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{item_id}", response_model=InventoryResponse)
async def update_inventory(
    item_id: str, update: InventoryUpdate, service=Depends(get_inventory_service)
):
    try:
        return await update_inventory_item(item_id, update, service)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
