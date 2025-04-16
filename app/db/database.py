from config import settings
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class Database:
    """
    A singleton database class to manage MongoDB connections using Motor.

    Attributes:
        db_client (AsyncIOMotorClient): Asynchronous MongoDB client instance
        _db (AsyncIOMotorDatabase): Database instance for the application
    """

    db_client: AsyncIOMotorClient
    _db: AsyncIOMotorDatabase

    @classmethod
    def connect(cls):
        """
        Establishes a singleton MongoDB connection.
        Creates a new client connection if one doesn't exist.
        Uses connection settings from the config file.
        """
        if not hasattr(cls, "db_client"):
            # Initialize the MongoDB client with the connection URI
            cls.db_client = AsyncIOMotorClient(settings.MONGO_URI)
            # Get reference to the specified database
            cls._db = cls.db_client[settings.DB_NAME]

    @classmethod
    def close(cls):
        """
        Closes the MongoDB connection and cleans up resources.
        Removes the client and database references from the class.
        """
        if hasattr(cls, "db_client"):
            # Close the MongoDB connection
            cls.db_client.close()
            # Remove references to allow garbage collection
            del cls.db_client
            del cls._db


async def start_db():
    """
    Initialize the database connection.
    Should be called when the application starts.
    """
    Database.connect()


async def shutdown_db_client():
    """
    Cleanup database connections.
    Should be called when the application shuts down.
    """
    Database.close()
