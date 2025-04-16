# core/logistics_logic.py

from app.models.logistics_schema import (
    LogisticsRequest,
    LogisticsPlanResponse,
    DeliveryRoute,
)
from motor.motor_asyncio import AsyncIOMotorCollection
from uuid import uuid4


async def generate_logistics_plan(
    request: LogisticsRequest, service: AsyncIOMotorCollection
) -> LogisticsPlanResponse:
    # Placeholder logic – simple round-robin distribution
    routes = []
    deliveries = request.deliveries
    sources = request.sources

    if not sources:
        raise ValueError("No sources provided for logistics planning.")

    for idx, delivery in enumerate(deliveries):
        source = sources[idx % len(sources)]
        route = DeliveryRoute(
            route_id=str(uuid4()),
            source=source,
            destination=delivery.destination,
            items=delivery.items,
        )
        routes.append(route)

    await service.insert_one(
        {"plan_id": str(uuid4()), "routes": [route.model_dump() for route in routes]}
    )

    return LogisticsPlanResponse(routes=routes)
