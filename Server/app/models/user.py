from pydantic import BaseModel
from typing import Optional
from uuid import uuid4

class User(BaseModel):
    id: str = str(uuid4())
    username: str
    email: str
    password: str
    birthday: Optional[str] = None
    is_active: bool = True
    full_name: Optional[str] = None
