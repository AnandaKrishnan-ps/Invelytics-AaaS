# api/surplus.py

from fastapi import APIRouter, Depends, HTTPException
from models.surplus_schema import SurplusRequest, SurplusMatchResponse
from core.surplus_logic import match_surplus_with_demand
from dependencies.surplus_deps import get_surplus_service

router = APIRouter()


@router.post("/match", response_model=SurplusMatchResponse)
async def match_surplus(
    surplus_request: SurplusRequest, surplus_service=Depends(get_surplus_service)
):
    try:
        result = await match_surplus_with_demand(surplus_request, surplus_service)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
