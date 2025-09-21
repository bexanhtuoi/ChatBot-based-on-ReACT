from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import uuid4, UUID


class ChatBase(BaseModel):
    user_id: UUID
    id: UUID = Field(default_factory=lambda: str(uuid4()))
    conversation: List[Optional[str]] = []
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    is_pro: bool = False
    is_private: bool = True

class SendMessage(BaseModel):
    id_chat: UUID
    message: str

class ChatUpdate(BaseModel):
    is_pro: Optional[bool]
    is_private: Optional[bool]