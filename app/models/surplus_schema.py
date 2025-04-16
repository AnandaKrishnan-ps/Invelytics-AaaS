# models/surplus_schema.py

from typing import Dict, List

from pydantic import BaseModel


class SurplusItem(BaseModel):
    item_id: str
    quantity: int


class SurplusRequest(BaseModel):
    surplus_items: List[SurplusItem]


class SurplusMatchResponse(BaseModel):
    match_id: str
    matched_demand: List[Dict[str, str]]
