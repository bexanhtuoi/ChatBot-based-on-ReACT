from app.database.database import DB
from app.schemas.chat import ChatBase, SendMessage
from typing import Optional, List
from app.crud.base import CRUDRepository

Collection = DB["chat"]

# CRUD Chat operations
class ChatCRUD(CRUDRepository):
    def __init__(self):
        super().__init__(Collection,  ChatBase, ChatBase)

    def get_chats_by_user(self, user_id: str) -> List[Optional[ChatBase]]:
        cursor = self.collection.find({"user_id": user_id})
        return [self.ReadSchema(**obj) for obj in cursor]

chat_crud = ChatCRUD()