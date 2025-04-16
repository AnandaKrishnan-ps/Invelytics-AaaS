# api/logistics.py

from typing import Any
from app.core.logistics_logic import generate_logistics_plan
from app.dependencies.logistics_deps import get_logistics_service
from app.models.logistics_schema import LogisticsPlanResponse, LogisticsRequest
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.post("/optimize", response_model=LogisticsPlanResponse)
async def optimize_logistics(
    request: LogisticsRequest, service:Any=Depends(get_logistics_service)
) -> LogisticsPlanResponse:
    try:
        return await generate_logistics_plan(request, service)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
