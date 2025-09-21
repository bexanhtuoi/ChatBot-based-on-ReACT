from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from app.core.config import settings
import certifi

uri = settings.mongo_uri

client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())

DB = client["ChatbotDB"]