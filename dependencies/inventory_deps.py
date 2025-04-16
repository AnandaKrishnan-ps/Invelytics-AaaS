# dependencies/inventory_deps.py


from db.database import Database


async def get_inventory_service():
    """Provides the inventory service (MongoDB collection)"""
    return Database._db.inventory
