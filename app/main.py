from fastapi import FastAPI
from app.database.database import db, redis_client
from fastapi.middleware.cors import CORSMiddleware
from app.api.websocket import router as ws_router
from app.api.routes import router as routes_router
import logging

app = FastAPI(
    title="Collaborative Whiteboard API",
    description="APIs for managing users, rooms, and WebSockets",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI (default: /docs)
    redoc_url="/redoc",  # ReDoc UI (default: /redoc)
)

# CORS settings (Adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register WebSocket router
app.include_router(ws_router)
app.include_router(routes_router)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup_event():
    """Logs database connection status on startup."""
    try:
        # Check MongoDB connection
        await db.command("ping")  # Pings MongoDB
        logger.info("✅ MongoDB is running and reachable!")
    except Exception as e:
        logger.error(f"❌ MongoDB is not reachable: {str(e)}")

    try:
        # Check Redis connection
        await redis_client.ping()  # Pings Redis
        logger.info("✅ Redis is running and reachable!")
    except Exception as e:
        logger.error(f"❌ Redis is not reachable: {str(e)}")


@app.get("/")
async def root():
    return {
        "message": "Welcome to the Collaborative Whiteboard Backend! Server is running"
    }
