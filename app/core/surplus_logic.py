# core/surplus_logic.py

from uuid import uuid4

from app.models.surplus_schema import SurplusMatchResponse, SurplusRequest
from motor.motor_asyncio import AsyncIOMotorCollection


async def match_surplus_with_demand(
    surplus_request: SurplusRequest, service: AsyncIOMotorCollection
) -> SurplusMatchResponse:
    """
    Matches surplus inventory items with demand based on request parameters.
    Simple logic to find matching demand for surplus items.
    """
    matched_demand = []
    surplus_items = surplus_request.surplus_items

    for item in surplus_items:
        demand_item = await service.find_one({"item_id": item.item_id})

        if demand_item and demand_item["quantity"] >= item.quantity:
            matched_demand.append(
                {
                    "item_id": item.item_id,
                    "quantity_matched": item.quantity,
                    "demand_id": demand_item["demand_id"],
                }
            )
        else:
            matched_demand.append(
                {"item_id": item.item_id, "quantity_matched": 0, "demand_id": None}
            )

    # Optionally store the result or log the matching in MongoDB
    match_id = str(uuid4())
    await service.insert_one({"match_id": match_id, "matched_demand": matched_demand})

    return SurplusMatchResponse(match_id=match_id, matched_demand=matched_demand)
