from app.database.database import redis_client
import logging

logger = logging.getLogger(__name__)


async def add_user_to_room(user_id: str, room_id: str):
    """Adds a user to an active room in Redis."""
    await redis_client.hset("active_users", user_id, room_id)
    logger.info(f"User {user_id} added to Redis for room {room_id}")


async def remove_user_from_room(user_id: str):
    """Removes a user from Redis when they disconnect."""
    await redis_client.hdel("active_users", user_id)
    logger.info(f"User {user_id} removed from Redis")


async def get_active_users(room_id: str):
    """Fetches all active users in a given room from Redis."""
    users = await redis_client.hgetall("active_users")
    return [user for user, room in users.items() if room == room_id]
