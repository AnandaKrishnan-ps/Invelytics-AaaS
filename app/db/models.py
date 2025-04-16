# db/models.py

from typing import Dict, List, Optional

from bson import ObjectId
from pydantic import BaseModel


class InventoryItem(BaseModel):
    item_id: str
    name: str
    description: Optional[str] = None
    quantity: int
    price: float
    category: Optional[str] = None

    class Config:
        json_encoders = {ObjectId: str}


class SurplusItem(BaseModel):
    item_id: str
    quantity: int
    price: float

class SurplusRequest(BaseModel):
    surplus_items: List[SurplusItem]


class SurplusMatchResponse(BaseModel):
    match_id: str
    matched_demand: List[Dict[str, str]]
