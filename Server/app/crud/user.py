from app.database.database import DB
from app.schemas.user import UserInDB, UserOut, UserUpdate
from typing import Optional, List
from app.security import verify_password
from app.crud.base import CRUDRepository

Collection = DB["user"]

# CRUD User operations
class UserCRUD(CRUDRepository):
    def __init__(self):
        super().__init__(Collection,  UserOut, UserUpdate)
    

    def authenticate_user(self, email: str, password: str) -> Optional[UserInDB]:
        user = Collection.find_one({"email": email})
        if not user:
            return None
        if not verify_password(password, user["hashed_password"]):
            return None
        return UserInDB(**user)


    def is_user_by_email(self, email: str) -> bool:
        return bool(Collection.find_one({"email": email}))


    def get_user_by_email(self, email: str) -> Optional[UserOut]:
        user = Collection.find_one({"email": email})
        return UserOut(**user) if user else None

user_crud = UserCRUD()