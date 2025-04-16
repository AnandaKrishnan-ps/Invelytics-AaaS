# main.py

from app import (
    inventory_router,
    logistics_router,
    recommendations_router,
    surplus_router,
)
from config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from lifespan import lifespan

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0", lifespan=lifespan)

# Allow CORS for testing/frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(inventory_router, prefix="/api/inventory", tags=["Inventory"])
app.include_router(surplus_router, prefix="/api/surplus", tags=["Surplus"])
app.include_router(logistics_router, prefix="/api/logistics", tags=["Logistics"])
app.include_router(
    recommendations_router, prefix="/api/recommendations", tags=["Recommendations"]
)


@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse("/docs")
