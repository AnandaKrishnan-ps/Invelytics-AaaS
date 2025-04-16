# dependencies/logistics_deps.py

from app.db.database import Database


def get_logistics_service():
    """Provides the logistics service (MongoDB collection)"""
    return Database._db.logistics
