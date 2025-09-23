from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from app.schemas.chat import ChatBase, SendMessage, ChatUpdate
from app.crud.chat import chat_crud
from app.api.dependencies import get_pagination_params, get_token
from datetime import datetime, timedelta
from app.ai.agent import Agent
from langchain_core.messages import HumanMessage, AIMessage

router = APIRouter()
agent = Agent()

@router.get(
    "all", response_model=List[Optional[ChatBase]], status_code=status.HTTP_200_OK
)
def fetch_all_chats(pagination: tuple = Depends(get_pagination_params)):
    skip, limit = pagination
    chats = chat_crud.get_many(skip=skip, limit=limit)
    chats = [chat for chat in chats if chat.is_private == False]
    return chats


@router.get(
    "/{chat_id}", response_model=Optional[ChatBase], status_code=status.HTTP_200_OK
)
def fetch_chat_by_id(chat_id: str, id_user: str = Depends(get_token)):
    chat = chat_crud.get_one(chat_id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat with id {chat_id} not found"
        )
    
    if chat.is_private:
        if chat.user_id != id_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )
    return chat


@router.get(
    "/u/{user_id}", response_model=List[Optional[ChatBase]], status_code=status.HTTP_200_OK
)
def fetch_chats_by_user_id(user_id: str, id_user: str = Depends(get_token)):
    if user_id != id_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )
    return chat_crud.get_chats_by_user(user_id)

@router.delete(
    "/{chat_id}", status_code=status.HTTP_200_OK, response_model=dict
)
def delete_chat(chat_id: str, id_user: str = Depends(get_token)):
    chat = chat_crud.get_one(chat_id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat with id {chat_id} not found"
        )
    if chat.user_id != id_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )
    try:
        chat_crud.delete(chat_id)
    except Exception as e: 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Couldn't delete chat with id {chat_id}. Error: {str(e)}",
        )
    return {"message": f"Chat with id {chat_id} deleted successfully."}

@router.post(
    "/", response_model=dict, status_code=status.HTTP_201_CREATED
)
async def send_chat(chat: SendMessage, id_user: str = Depends(get_token)):
    chat_data = chat_crud.get_one(chat.id_chat)
    print(chat_data)
    if not chat_data:
        chat_data = chat.model_dump()

        message = HumanMessage(content=chat_data["message"])
        response = await agent.invoke(chat_data["message"], [])
        conversation = [message, AIMessage(content=response["output"])]

        chat_in_db = ChatBase(
            conversation=conversation,
            user_id=id_user,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        )
        chat_crud.create_one(chat_in_db)
        return {"message": "Chat created successfully", "response": response["output"]}
    
    if chat_data.user_id != id_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )
    message = HumanMessage(content=chat.message)
    history = []
    for msg in chat_data.conversation:
        if msg is not None:
            if "AI:" in msg:
                history.append(AIMessage(content=msg.replace("AI: ", "")))
            elif "Human:" in msg:
                history.append(HumanMessage(content=msg.replace("Human: ", "")))

    response = await agent.invoke(chat.message, history)

    chat_data.conversation.append(message)
    chat_data.conversation.append(AIMessage(content=response["output"]))
    chat_data.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chat_crud.update(chat_data.id, chat_data)
    return {"message": "Chat updated successfully", "response": response["output"]}

@router.put(
    "/{chat_id}", response_model=ChatBase, status_code=status.HTTP_200_OK
)
def update_chat(chat_id: str, update: ChatUpdate, id_user: str = Depends(get_token)):
    chat_in_db = chat_crud.get_one(chat_id)
    if not chat_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat with id {chat_id} not found"
        )
    if chat_in_db.user_id != id_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )
    chat_in_db.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chat_in_db.is_pro = update.is_pro if update.is_pro is not None else chat_in_db.is_pro
    chat_in_db.is_private = update.is_private if update.is_private is not None else chat_in_db.is_private
    chat = ChatBase(**chat_in_db.model_dump())

    try:
        chat_crud.update(chat_id, chat)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Couldn't update chat with id {chat_id}. Error: {str(e)}",
        )
    return chat
    

