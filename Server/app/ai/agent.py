from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from app.ai.rag import RAG
from typing import List, Union

from app.core.config import settings

class Agent(RAG):
    def __init__(self, model: str = "gemini-2.0-flash-lite", k: int = 3):
        super().__init__(folder_path="app/database/RAG_Document")
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=settings.gemini_api_key,
        )
        self.rag_tool = Tool(
            name="RAG Tool",
            func=self.retriver,
            description="Trả lời các câu hỏi dựa trên tài liệu nội bộ về công ty X ví dụ như ngày nghỉ, lịch nghỉ lễ hay chính sách công ty"
        )
        self.search_tool = Tool(
            name="Tavily Search",
            func=TavilySearchResults(k=k, api_key=settings.tavily_api_key),
            description="Tìm kiếm thông tin thời gian thực từ internet như thời tiết, giá vàng, tin tức."
        )
        self.tools = [
            self.search_tool,
            self.rag_tool
            ]

        self.agent = create_react_agent(llm=self.llm,
                                   tools=self.tools,
                                   prompt=self._get_prompt())

        self.agent_executor = AgentExecutor(agent=agent,
                                       tools=self.tools,
                                       handle_parsing_errors=True,
                                       max_iterations=10,
                                       max_execution_time=120,
                                       )

    def _get_prompt(self, template_path: str = "app/database/template.txt"):
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
        prompt = PromptTemplate.from_template(template)
        return prompt

    def _get_memory(self, chat_history: List[Union[HumanMessage, AIMessage]] = []):
        memory = ""
        for message in chat_history:
            if isinstance(message, HumanMessage):
                memory += f"Human: {message.content}\n"
            elif isinstance(message, AIMessage):
                memory += f"AI: {message.content}\n"
        return memory
        

    async def invoke(self, question: str, chat_history: List[Union[HumanMessage, AIMessage]] = []):
        memory = self._get_memory(chat_history)
        return await agent_executor.ainvoke({"input": question, "chat_history": memory})