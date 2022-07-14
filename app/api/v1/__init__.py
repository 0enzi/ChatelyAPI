from fastapi import APIRouter

from app.api.v1.users import  auth, user
from app.api.v1.chat import chat

api_router = APIRouter()
# api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
# api_router.include_router(sockets.router, prefix="/ws", tags=["sockets"])

