from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from app.schemas.user import UserOut, UserUpdate
from app.crud.user import user_crud
from app.api.dependencies import get_pagination_params, get_current_user

router = APIRouter()

@router.get(
    "/all", response_model=List[Optional[UserOut]], status_code=status.HTTP_200_OK
)
def fetch_all_users(pagination: tuple = Depends(get_pagination_params)):
    skip, limit = pagination
    return user_crud.get_many(skip=skip, limit=limit)

@router.get(
    "/{user_id}", response_model=Optional[UserOut], status_code=status.HTTP_200_OK
)
def fetch_user_by_id(user_id: str):
    user = user_crud.get_one(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user

@router.get(
    "/e/{email}", response_model=Optional[UserOut], status_code=status.HTTP_200_OK
)
def fetch_user_by_email(email: str):
    user = user_crud.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {email} not found"
        )
    return user

@router.delete(
    "/{user_id}", status_code=status.HTTP_200_OK, response_model=dict
)
def delete_user(user_id: str, current_user: UserOut = Depends(get_current_user)):
    user = user_crud.get_one(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    if user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )
    try:
        user_crud.delete(user_id)
    except Exception as e: 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Couldn't delete user with id {user_id}. Error: {str(e)}",
        ) from e
    return {"message": f"User with id {user_id} has been deleted"}

@router.put(
    "/{user_id}", status_code=status.HTTP_200_OK, response_model=dict
)
def update_user(
    user_id: str,
    user_update: UserUpdate,
    current_user: UserOut = Depends(get_current_user)):

    user = user_crud.get_one(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    if user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )
    try:
        user_crud.update(user_id, user_update)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Couldn't update user with id {user_id}. Error: {str(e)}",
        ) from e
    return {"message": f"User with id {user_id} has been updated"}