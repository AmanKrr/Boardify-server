import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException
from app.config import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_jwt_token(user_id: str) -> str:
    """Generates JWT token for user authentication."""
    expiration = datetime.utcnow() + timedelta(hours=config.JWT_EXPIRATION_HOURS)
    payload = {"user_id": user_id, "exp": expiration}
    return jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)


def verify_jwt_token(token: str):
    """Validates a JWT token and returns the user payload."""
    try:
        payload = jwt.decode(
            token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
