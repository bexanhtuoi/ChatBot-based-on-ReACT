from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import User
from app.database.database import users_collection
from passlib.context import CryptContext

router = APIRouter(tags=["register"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def iUserExists(username: str, email: str) -> bool:
    if users_collection.find_one({"$or": [{"username": username}, {"email": email}]}):
        return True
    return False

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: User):
    is_user_exists = isUserExists(user.username, user.email)
    
    if is_user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists."
        )
    try:
        user.password = hash_password(user.password)
        users_collection.insert_one(user.dict())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while registering the user: {str(e)}"
        )
    
    return {"message": "User registered successfully.", "status": status.HTTP_201_CREATED}