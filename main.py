# main.py

from app.api import inventory, logistics, recommendations, surplus
from config import settings
from lifespan import lifespan
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

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
app.include_router(inventory.router, prefix="/api/inventory", tags=["Inventory"])
app.include_router(surplus.router, prefix="/api/surplus", tags=["Surplus"])
app.include_router(logistics.router, prefix="/api/logistics", tags=["Logistics"])
app.include_router(
    recommendations.router, prefix="/api/recommendations", tags=["Recommendations"]
)


@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse("/docs")
