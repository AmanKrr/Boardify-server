from app.database.database import db
from app.models.room import RoomSchema
from passlib.hash import bcrypt
import logging

logger = logging.getLogger(__name__)


async def create_room(room_data: RoomSchema):
    """Creates a new room in MongoDB."""
    if room_data.is_private and room_data.password_hash:
        room_data.password_hash = bcrypt.hash(
            room_data.password_hash
        )  # Hashing password

    room = await db.rooms.insert_one(room_data.dict())
    logger.info(f"Room created: {room_data.name}")
    return str(room.inserted_id)


async def verify_room_password(room_id: str, plain_password: str):
    """Verifies if the given password matches the stored hashed password."""
    room = await db.rooms.find_one({"id": room_id})
    if room and bcrypt.verify(plain_password, room["password_hash"]):
        return True  # Password correct
    return False  # Password incorrect


async def get_room_by_id(room_id: str):
    """Fetches a room by ID."""
    room = await db.rooms.find_one({"id": room_id})
    if room:
        return RoomSchema(**room)
    return None


async def add_user_to_room(room_id: str, user_id: str):
    """Adds a user to an existing room."""
    await db.rooms.update_one({"id": room_id}, {"$push": {"users": user_id}})
    logger.info(f"User {user_id} added to room {room_id}")


async def remove_user_from_room(room_id: str, user_id: str):
    """Removes a user from a room and deletes empty rooms."""
    await db.rooms.update_one({"id": room_id}, {"$pull": {"users": user_id}})

    # Delete the room if empty
    room = await db.rooms.find_one({"id": room_id})
    if room and not room["users"]:
        await db.rooms.delete_one({"id": room_id})
        logger.info(f"Room {room_id} deleted as it's empty")
