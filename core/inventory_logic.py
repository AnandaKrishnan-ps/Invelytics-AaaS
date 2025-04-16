# core/inventory_logic.py

from datetime import UTC, datetime
from typing import List

from bson import ObjectId
from fastapi import HTTPException
from models.inventory_schema import InventoryItem, InventoryResponse, InventoryUpdate
from motor.motor_asyncio import AsyncIOMotorCollection


async def get_all_inventory_items(
    service: AsyncIOMotorCollection,
    limit: int = 10,
    skip: int = 0,
    ignore_limit: bool = False,
) -> List[InventoryResponse]:
    items = []
    try:
        if ignore_limit:
            limit = await service.count_documents({})
            skip = 0
    
        cursor = service.find().skip(skip).limit(limit)
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            items.append(InventoryResponse(**doc))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching inventory: {str(e)}"
        )
    return items


async def add_inventory_item(
    item: InventoryItem, service: AsyncIOMotorCollection
) -> InventoryResponse:
    item_dict = item.model_dump()
    item_dict["last_updated"] = datetime.now(UTC)
    result = await service.insert_one(item_dict)
    item_dict["id"] = str(result.inserted_id)
    return InventoryResponse(**item_dict)


async def update_inventory_item(
    item_id: str, update: InventoryUpdate, service: AsyncIOMotorCollection
) -> InventoryResponse:
    update_data = {k: v for k, v in update.model_dump().items() if v is not None}
    update_data["last_updated"] = datetime.now(UTC)  # update timestamp
    result = await service.find_one_and_update(
        {"_id": ObjectId(item_id)}, {"$set": update_data}, return_document=True
    )
    if result:
        result["id"] = str(result["_id"])
        return InventoryResponse(**result)
    raise ValueError("Inventory item not found")
