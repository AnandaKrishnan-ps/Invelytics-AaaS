from datetime import UTC, datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class InventoryItem(BaseModel):
    item_id: str
    name: str
    description: Optional[str] = None
    quantity: int
    price: float
    category: Optional[str] = None

    class Config:
        json_encoders = {ObjectId: str}


class InventoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    category: Optional[str] = None


class InventoryResponse(InventoryItem):
    id: str
    last_updated: datetime
