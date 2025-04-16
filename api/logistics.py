# api/logistics.py

from fastapi import APIRouter, Depends, HTTPException
from models.logistics_schema import LogisticsRequest, LogisticsPlanResponse
from core.logistics_logic import generate_logistics_plan
from dependencies.logistics_deps import get_logistics_service

router = APIRouter()


@router.post("/optimize", response_model=LogisticsPlanResponse)
async def optimize_logistics(
    request: LogisticsRequest, service=Depends(get_logistics_service)
):
    try:
        return await generate_logistics_plan(request, service)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
