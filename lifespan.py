# app/config/lifespan.py
from contextlib import asynccontextmanager
from typing import Any

from app.core.scheduler import start_scheduler
from app.db import shutdown_db_client, start_db
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:

    await start_db()
    start_scheduler()
    yield
    await shutdown_db_client()
