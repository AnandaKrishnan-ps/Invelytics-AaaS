# models/logistics_schema.py

from pydantic import BaseModel
from typing import List


class InventoryItem(BaseModel):
    item_id: str
    name: str
    quantity: int
    price: float


class DeliveryRequest(BaseModel):
    destination: str
    items: List[InventoryItem]


class LogisticsRequest(BaseModel):
    deliveries: List[DeliveryRequest]
    sources: List[str]


class DeliveryRoute(BaseModel):
    route_id: str
    source: str
    destination: str
    items: List[InventoryItem]


class LogisticsPlanResponse(BaseModel):
    routes: List[DeliveryRoute]
