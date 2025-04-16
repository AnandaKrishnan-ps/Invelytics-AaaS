# dependencies/inventory_deps.py


from app.db.database import Database
from motor.motor_asyncio import AsyncIOMotorCollection


async def get_inventory_service() -> AsyncIOMotorCollection:
    """Provides the inventory service (MongoDB collection)"""
    return Database._db.inventory

async def get_inventory_logs_service() -> AsyncIOMotorCollection:
    """Provides the sales service (MongoDB collection)"""
    return Database._db.inventory_logs
