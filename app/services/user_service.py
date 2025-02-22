from app.database.database import db
from app.models.user import UserSchema
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)


async def create_user(user_data: UserSchema):
    """Stores user details in MongoDB."""
    hashed_password = bcrypt.hash(user_data.password_hash)  # Hashing user password
    user_data.password_hash = hashed_password
    user = await db.users.insert_one(user_data.dict())
    logger.info(f"User created: {user_data.username}")
    return str(user.inserted_id)


async def verify_user_password(email: str, plain_password: str):
    """Verifies if the given password matches the stored hashed password."""
    user = await get_user_by_email(email)
    if user and bcrypt.verify(plain_password, user["password_hash"]):
        return user  # Authentication successful
    return None  # Authentication failed


async def get_user_by_email(email: str):
    """Fetches a user by email."""
    return await db.users.find_one({"email": email})


async def update_user_room(user_id: str, room_id: str):
    """Updates a user's current room."""
    await db.users.update_one({"id": user_id}, {"$set": {"current_room": room_id}})
    logger.info(f"User {user_id} moved to room {room_id}")


async def remove_user(user_id: str):
    """Deletes a user (cleanup when they disconnect)."""
    await db.users.delete_one({"id": user_id})
    logger.info(f"User {user_id} removed from MongoDB")
