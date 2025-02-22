from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis
from app.config import config
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connect to MongoDB
try:
    mongo_client = AsyncIOMotorClient(config.MONGO_URI)
    db = mongo_client[config.MONGO_DB_NAME]
    logger.info("✅ MongoDB connection established successfully!")
except Exception as e:
    logger.error(f"❌ MongoDB connection failed: {str(e)}")

# Connect to Redis
try:
    redis_client = Redis.from_url(config.REDIS_URI, decode_responses=True)
    logger.info("✅ Redis connection established successfully!")
except Exception as e:
    logger.error(f"❌ Redis connection failed: {str(e)}")
