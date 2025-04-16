# dependencies/logistics_deps.py

from app.db.database import Database
from motor.motor_asyncio import AsyncIOMotorCollection


def get_logistics_service() -> AsyncIOMotorCollection:
    """Provides the logistics service (MongoDB collection)"""
    return Database._db.logistics
