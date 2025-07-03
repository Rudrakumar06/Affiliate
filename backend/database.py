from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import os

# Database connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db_name = os.environ.get('DB_NAME', 'affiliate_marketing')
database = client[db_name]

async def get_database() -> AsyncIOMotorDatabase:
    """Dependency to get database instance"""
    return database

async def close_database_connection():
    """Close database connection"""
    client.close()