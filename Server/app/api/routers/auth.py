from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth import UserRegister
from app.schemas.user import UserInDB
from app.crud.user import user_crud
from app.security import hash_password
from app.core.config import settings
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.security import create_access_token


router = APIRouter()

@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
def register(user: UserRegister):
    is_user_exists = user_crud.is_user_by_email(user.email)
    
    if is_user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The user with this {user.email} already exists in the system"
        )
    try:
        user_data = user.model_dump(exclude={"password"})
        user_in_db = UserInDB(
            **user_data,
            hashed_password=hash_password(user.password),
            day_created=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        user_crud.create_one(user_in_db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while registering the user: {str(e)}"
        )
    
    return {"message": "User registered successfully."}


@router.post("/token", response_model=dict, status_code=status.HTTP_200_OK)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_crud.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    access_token_expires = timedelta(minutes=settings.access_token_expires_minutes)
    access_token = create_access_token(
        data=user.id, expires_delta=access_token_expires
    )
    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(key="access_token",
            value=access_token,
            httponly=True, 
            secure=False,
            samesite="lax",
)
    return response

@router.post("/logout", response_model=dict, status_code=status.HTTP_200_OK)
def logout():
    response = JSONResponse(content={"message": "Logout successful"})
    response.delete_cookie(key="access_token")
    return response