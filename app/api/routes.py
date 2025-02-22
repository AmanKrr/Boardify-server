from fastapi import APIRouter, HTTPException
from app.models.room import RoomSchema
from app.services.room_service import create_room

router = APIRouter()


@router.post("/rooms/private/create", tags=["Rooms"], summary="Create a Private Room")
async def create_private_room(room: RoomSchema):
    """
    Creates a private room with a hashed password.

    ### Request Body:
    - **name**: The name of the private room (string).
    - **is_private**: Boolean indicating if the room is private.
    - **password_hash**: The password for the private room (sent as plaintext, backend hashes it).

    ### Response:
    - **room_id**: The unique ID of the created room.
    - **message**: Confirmation message.

    **Error Responses:**
    - `400`: If password is missing.
    """
    if not room.password_hash:
        raise HTTPException(
            status_code=400, detail="Password is required for private rooms"
        )

    room_id = await create_room(room)
    return {"message": "Private room created", "room_id": room_id}
