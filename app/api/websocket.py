from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from app.services.connection_manager import manager
from app.services.user_service import update_user_room
from app.services.room_service import add_user_to_room, get_room_by_id
from app.utils.security import verify_jwt_token
from app.services.redis_service import get_active_users
import json
import uuid
import logging
from app.config import config

router = APIRouter()
logger = logging.getLogger(__name__)

# In-memory public rooms tracking
public_rooms = {"public-1": []}
MAX_USERS = config.MAX_PUBLIC_ROOM_USERS


@router.websocket("/ws/public")
async def public_ws(websocket: WebSocket):
    """Handles WebSocket connection for public rooms and saves user-room mapping in MongoDB."""
    global public_rooms

    # Find an available room
    room_id = next(
        (room for room, users in public_rooms.items() if len(users) < MAX_USERS), None
    )

    print(room_id)
    print(MAX_USERS)

    # If no room is available, create a new public room
    if not room_id:
        room_id = f"public-{len(public_rooms) + 1}"
        public_rooms[room_id] = []

    user_id = str(uuid.uuid4())
    public_rooms[room_id].append(user_id)

    await manager.connect(websocket, room_id, user_id)
    await add_user_to_room(room_id, user_id)  # Store in MongoDB
    await update_user_room(user_id, room_id)  # Store user-room mapping
    active_users = await get_active_users(room_id)
    await manager.broadcast(
        json.dumps(
            {
                "type": "users",
                "userId": user_id,
                "activeUsers": active_users,
                "roomId": room_id,
            }
        ),
        room_id,
    )
    # await manager.broadcast(f"User {user_id} joined {room_id}", room_id)
    logger.info(f"User {user_id} connected to public room {room_id}")

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data, room_id)

    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id, user_id)
        public_rooms[room_id].remove(user_id)
        logger.info(f"User {user_id} disconnected from public room {room_id}")


@router.websocket("/ws/private/{room_id}")
async def private_ws(websocket: WebSocket, room_id: str, user_id: str = Query(...)):
    print("hit")
    """Handles private WebSocket connection, verifies user authentication, and stores data in MongoDB."""
    try:
        # Check if room exists in MongoDB
        room = await get_room_by_id(room_id)
        if not room:
            await websocket.close()
            return

        await manager.connect(websocket, room_id, user_id)
        await add_user_to_room(room_id, user_id)  # Store in MongoDB
        active_users = await get_active_users(room_id)
        await manager.broadcast(
            json.dumps(
                {"type": "users", "activeUsers": active_users, "roomId": room_id}
            ),
            room_id,
        )
        logger.info(f"User {user_id} joined private room {room_id}")

        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data, room_id)

    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id, user_id)
        logger.info(f"User {user_id} disconnected from private room {room_id}")
