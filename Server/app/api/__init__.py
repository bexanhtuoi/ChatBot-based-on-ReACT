from app.api.routers.auth import router as auth_router
from app.api.routers.user import router as user_router
from app.api.routers.chat import router as chat_router

__all__ = ["auth_router", "user_router", "chat_router"]