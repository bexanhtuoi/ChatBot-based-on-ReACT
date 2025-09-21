import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, HTTPException, status, Cookie, Query, Depends
from typing import Annotated, Tuple
from pydantic import ValidationError
from app.core.config import settings
from app.schemas.user import UserOut
from app.crud.user import user_crud

def get_token(access_token: Annotated[str, Cookie()] = None) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not access_token:
        raise credentials_exception

    try:
        payload = jwt.decode(access_token, settings.secret_key, algorithms=[settings.algorithm])
        token_data = payload.get("sub")

        if token_data is None:
            raise credentials_exception

    except (InvalidTokenError, ValidationError):
        raise credentials_exception

    return token_data

def get_pagination_params(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1)
) -> Tuple[int, int]:
    return skip, limit

def get_current_user(user_id: str = Depends(get_token)) -> UserOut: 
    user = user_crud.get_one(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found with your access token"
        )
    return user