from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import uuid4, UUID


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserInDB(UserBase):
    id: UUID = Field(default_factory=lambda: str(uuid4()))
    hashed_password: str
    day_created: Optional[str] = None
    is_active: bool = True

class UserOut(UserBase):
    id: UUID
    day_created: Optional[str] = None
    is_active: bool = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None