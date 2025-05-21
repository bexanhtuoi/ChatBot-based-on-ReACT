from ..models.response import Response
from fastapi import APIRouter, HTTPException
import json
import os
from dotenv import load_dotenv
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import PromptTemplate
from ..services.rag import RAG
from langchain.memory import ConversationBufferMemory
import asyncio
from concurrent.futures import ThreadPoolExecutor


router = APIRouter()

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite",
    google_api_key=GEMINI_API_KEY,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAG_ = RAG(folder_path= os.path.join(BASE_DIR, "RAG_Document"))

rag_tool = Tool(
    name="RAG Tool",
    func=RAG_.retriver,
    description="Trả lời các câu hỏi dựa trên tài liệu nội bộ về công ty X ví dụ như ngày nghỉ, lịch nghỉ lễ hay chính sách công ty"
)


search_tool = Tool(
    name="Tavily Search",
    func=TavilySearchResults(k=3, api_key=TAVILY_API_KEY),
    description="Tìm kiếm thông tin thời gian thực từ internet như thời tiết, giá vàng, tin tức."
)

tools = [search_tool, rag_tool]

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "template.txt")
with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
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

@router.get("/response")
async def get_response():
    data_path = os.path.join(os.path.dirname(__file__), "data.json")
    with open(data_path, 'r') as f:
        loaded = json.load(f)
        if loaded != []:
            data = loaded[-1]
        else:
            raise HTTPException(status_code=404, detail="No data found")

    mes = Response(text=data["text"],
                    timestamp=data["timestamp"])
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        responsive = await loop.run_in_executor(pool, agent_executor.invoke, {"input": mes.text})
    return {"status_code": 200,
        "message": "Response retrieved successfully",
        "data": responsive
    }