from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    cors_origins: list[str] = os.getenv("CORS_ORIGINS")
    mongo_uri: str = os.getenv("MONGO_URI")
    secret_key: str = os.getenv("MY_SECRET_KEY")
    algorithm: str = os.getenv("ALGORITHM")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY")
    tavily_api_key: str = os.getenv("TAVILY_API_KEY")
    access_token_expires_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 120))

settings = Settings()
