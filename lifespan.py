# app/config/lifespan.py
from contextlib import asynccontextmanager

from app.db import shutdown_db_client, start_db
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):

    await start_db()
    yield
    await shutdown_db_client()
