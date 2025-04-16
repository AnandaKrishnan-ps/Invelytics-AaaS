from typing import List

from app.models.logs_schema import InventoryLogResponse
from motor.motor_asyncio import AsyncIOMotorCollection


async def get_logs_service(
    log_service: AsyncIOMotorCollection,
    limit: int = 50,
    offset: int = 0,
    sort_by: str = "date",
    sort_order: str = "desc",
) -> List[InventoryLogResponse]:
    sort_dir = -1 if sort_order.lower() == "desc" else 1
    cursor = log_service.find().sort(sort_by, sort_dir).skip(offset).limit(limit)
    logs = await cursor.to_list(length=limit)
    return [InventoryLogResponse(id=str(log["_id"]), **log) for log in logs]
