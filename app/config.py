import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    # Database Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "whiteboard_app")

    # Redis Configuration
    REDIS_URI = os.getenv("REDIS_URI", "redis://localhost:6379")

    # JWT Authentication
    JWT_SECRET = os.getenv("JWT_SECRET", "your_secret_key")
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", 2))

    # WebSocket Configuration
    MAX_PUBLIC_ROOM_USERS = int(os.getenv("MAX_PUBLIC_ROOM_USERS", 50))


config = Config()
