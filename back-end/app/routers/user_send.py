from ..models.chat import Chat
from fastapi import APIRouter, Form
import json
import os
from datetime import datetime

router = APIRouter()

async def save_chat_to_file(chat: Chat):
    data_path = os.path.join(os.path.dirname(__file__), "data.json")
    if not os.path.exists(data_path):
        data = []
    else:
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    data.append(chat.dict())
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@router.post("/chat")
async def send_chat(chat: str = Form(...)):
    chat = Chat(text=chat, timestamp=datetime.now().isoformat())
    await save_chat_to_file(chat)
    return {"status_code": 200, "message": "Chat message sent successfully", "data": chat}