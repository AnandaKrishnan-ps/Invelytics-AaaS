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


class DeliveryRequest(BaseModel):
    destination: str
    items: List[InventoryItem]


class LogisticsRequest(BaseModel):
    deliveries: List[DeliveryRequest]
    sources: List[str]


class LogisticsPlanResponse(BaseModel):
    route_id: str
    source: str
    destination: str
    items: List[InventoryItem]


class SurplusMatchResponse(BaseModel):
    match_id: str
    matched_demand: List[Dict[str, str]]
