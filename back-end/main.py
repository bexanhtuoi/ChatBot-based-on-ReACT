from fastapi import FastAPI
from app.routers import server_response, user_send
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

app.include_router(server_response.router, prefix="/api")
app.include_router(user_send.router, prefix="/api")
