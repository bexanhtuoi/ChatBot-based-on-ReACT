from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from app.core.config import settings

uri = settings.mongo_uri

client = MongoClient(uri, server_api=ServerApi('1'))

db = client["exampledb"]

users_collection = db["users_chatbotapp"]

chat_collection = db["chats"]