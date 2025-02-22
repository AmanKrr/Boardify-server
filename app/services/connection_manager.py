from fastapi import WebSocket
from app.services.redis_service import (
    add_user_to_room,
    remove_user_from_room,
    get_active_users,
)
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        """Manages active WebSocket connections per room."""
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, room_id: str, user_id: str):
        """Accepts a WebSocket connection and adds user to the active room."""
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append((websocket, user_id))
        await add_user_to_room(user_id, room_id)
        logger.info(f"User {user_id} connected to {room_id}")

    def disconnect(self, websocket: WebSocket, room_id: str, user_id: str):
        """Removes a WebSocket connection from a room and cleans up empty rooms."""
        if room_id in self.active_connections:
            self.active_connections[room_id] = [
                (ws, uid)
                for ws, uid in self.active_connections[room_id]
                if ws != websocket
            ]
            if not self.active_connections[room_id]:  # Remove empty room
                del self.active_connections[room_id]
        remove_user_from_room(user_id)
        logger.info(f"User {user_id} disconnected from {room_id}")

    async def broadcast(self, message: str, room_id: str):
        """Sends a message to all users in a room."""
        if room_id in self.active_connections:
            # Create a copy of the connections list to iterate over
            connections = self.active_connections[room_id][:]
            for websocket, user_id in connections:
                try:
                    await websocket.send_text(message)
                except RuntimeError as e:
                    if 'Cannot call "send" once a close message has been sent.' in str(
                        e
                    ):
                        logger.warning(
                            f"Removing closed connection for user {user_id} in room {room_id}."
                        )
                        # Remove the closed connection
                        self.active_connections[room_id].remove((websocket, user_id))
                        # Optionally, update your state if needed, e.g., call remove_user_from_room(user_id)
                    else:
                        raise  # Re-raise if it's an unexpected error
            logger.info(f"Broadcasted message to {room_id}: {message}")


# Singleton instance of ConnectionManager
manager = ConnectionManager()
