from db import shutdown_db_client, start_db
from fastapi import FastAPI, logger


async def lifespan(app: FastAPI):
    
    print("Starting up...")
    start_db()
    yield
    print("Shutting down...")
    shutdown_db_client()
