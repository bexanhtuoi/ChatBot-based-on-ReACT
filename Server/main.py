from fastapi import FastAPI
from app.routers import chat, user, login, register
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Chatbot API"}

app.include_router(chat.router)
app.include_router(user.router)
app.include_router(login.router)
app.include_router(register.router)
