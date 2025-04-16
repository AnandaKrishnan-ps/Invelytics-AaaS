# dependencies/surplus_deps.py

from app.db.database import Database


def get_surplus_service():
    """Provides the surplus service (MongoDB collection)"""
    return Database._db.surplus
