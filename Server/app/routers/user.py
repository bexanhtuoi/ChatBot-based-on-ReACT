from fastapi import APIRouter, Depends, HTTPException, status, Cookie
from typing import Annotated
from app.database.database import chat_collection
import jwt
from jwt.exceptions import InvalidTokenError
from app.core.config import settings
import json

router = APIRouter(prefix="/api", tags=["user_chat"])

def authenticate_user(access_token: Annotated[str, Cookie()] = None):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not access_token:
        raise credentials_exception

    try:
        payload = jwt.decode(access_token, settings.secret_key, algorithms=[settings.algorithm])
        user = payload.get("user")
        if user is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    return user

@router.get("/{user_id}")
def get_user_chat(user_id: str, current_user: dict = Depends(authenticate_user)):

    user = current_user.get("user")
    user_id = user.get("user_id")

    result = chat_collection.find_one(
        {"user_id": user_id},
        {"all_chat.id_chat": 1, "_id": 0})

    if result:
        id_chats = [chat["id_chat"] for chat in result["all_chat"]]
    return {
        "status_code": status.HTTP_200_OK,
        "id_chats": id_chats,
        "user_name": current_user.get("user_name")
    }
