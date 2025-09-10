# Import models

# Import FastAPI modules
from fastapi import APIRouter, HTTPException, status, Cookie, Depends
from typing import Annotated
from app.database.database import chat_collection
from app.routers.user import authenticate_user

# Import environment variables
from app.core.config import settings

# Import langchain modules
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import PromptTemplate
from app.services.rag import RAG
from langchain.memory import ConversationBufferMemory

# Other imports
import asyncio
from datetime import datetime
from uuid import uuid4

router = APIRouter(prefix="/api", tags=["chat"])


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite",
    google_api_key=settings.gemini_api_key,
)

doc_dir = "app/database/RAG_Document"
rag = RAG(folder_path= doc_dir)

rag_tool = Tool(
    name="RAG Tool",
    func=rag.retriver,
    description="Trả lời các câu hỏi dựa trên tài liệu nội bộ về công ty X ví dụ như ngày nghỉ, lịch nghỉ lễ hay chính sách công ty"
)


search_tool = Tool(
    name="Tavily Search",
    func=TavilySearchResults(k=3, api_key=settings.tavily_api_key),
    description="Tìm kiếm thông tin thời gian thực từ internet như thời tiết, giá vàng, tin tức."
)

tools = [search_tool, rag_tool]

template_path = "app/database/template.txt"
with open(template_path, "r", encoding="utf-8") as f:
    template = f.read()

prompt = PromptTemplate.from_template(template)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


agent = create_react_agent(llm=llm,
                           tools=tools,
                           prompt=prompt)


agent_executor = AgentExecutor(agent=agent,
                               tools=tools,
                               handle_parsing_errors=True,
                               max_iterations=10,
                               max_execution_time=120,
                               memory=memory
                               )

def save_chat_to_db(user_id: str, id_chat: str, message: str, response: str):
    new_messages = [
        {"role": "user", "content": message, "timestamp": datetime.utcnow()},
        {"role": "assistant", "content": response, "timestamp": datetime.utcnow()}
    ]
    try:
        result = chat_collection.update_one(
            {"user_id": user_id, "all_chat.id_chat": id_chat},
            {"$push": {"all_chat.$.messages": {"$each": new_messages}}}
        )

        if result.matched_count == 0:
            # Nếu chat chưa tồn tại, tạo mới
            chat_collection.update_one(
                {"user_id": user_id},
                {"$push": {"all_chat": {"id_chat": id_chat, "messages": new_messages}}},
                upsert=True
            )
        return True
    except Exception as e:
        print(f"An error occurred while saving chat to DB: {str(e)}")
        return False

@router.post("/chat")
async def chat(message: str, id_chat: str = str(uuid4), current_user: dict = Depends(authenticate_user)):
    user = current_user
    user_id = user.get("user_id")
    try:
        responsive =  await asyncio.to_thread(agent_executor.invoke, {"input": message})
        response_text = responsive['output']
        Is_saved = await asyncio.to_thread(save_chat_to_db, user_id, id_chat, message, response_text)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the chat: {str(e)}"
        )
    return {"status_code": status.HTTP_200_OK,
        "message": "Response retrieved successfully",
        "data": response_text
    }