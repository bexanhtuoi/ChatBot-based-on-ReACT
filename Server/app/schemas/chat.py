from pydantic import BaseModel, Field
from typing import Optional, List, Union
from langchain_core.messages import HumanMessage, AIMessage



class ChatBase(BaseModel):
    user_id: str
    id: str 
    conversation: List[Union[HumanMessage, AIMessage]] = []
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    is_pro: bool = False
    is_private: bool = False

class SendMessage(BaseModel):
    message: str

class ChatUpdate(BaseModel):
    is_pro: Optional[bool]
    is_private: Optional[bool]