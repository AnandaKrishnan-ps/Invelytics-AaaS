# dependencies/surplus_deps.py

from app.db.database import Database
from motor.motor_asyncio import AsyncIOMotorCollection

def get_surplus_service() -> AsyncIOMotorCollection:
    """Provides the surplus service (MongoDB collection)"""
    return Database._db.surplus
