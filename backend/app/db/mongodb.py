from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class Database:
    client: AsyncIOMotorClient = None

    def connect(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)

    def close(self):
        self.client.close()

db = Database()

def get_database():
    return db.client[settings.DATABASE_NAME]