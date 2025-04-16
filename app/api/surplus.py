# api/surplus.py

from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from app.models.surplus_schema import SurplusRequest, SurplusMatchResponse
from app.core.surplus_logic import match_surplus_with_demand
from app.dependencies.surplus_deps import get_surplus_service

router = APIRouter()


@router.post("/match", response_model=SurplusMatchResponse)
async def match_surplus(
    surplus_request: SurplusRequest, surplus_service:Any=Depends(get_surplus_service)
) -> SurplusMatchResponse:
    try:
        result = await match_surplus_with_demand(surplus_request, surplus_service)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
