from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel

from app.core.enums import InventoryChangeCategory, UpdatedByCategory


class InventoryLog(BaseModel):
    item_id: str
    date: datetime
    field: str
    old_quantity: int
    updated_quantity: int
    category: InventoryChangeCategory
    updated_by: UpdatedByCategory

    class Config:
        json_encoders = {ObjectId: str}


class InventoryLogResponse(InventoryLog):
    id: Optional[str]
