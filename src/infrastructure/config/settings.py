from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    USE_MONGODB: bool = False
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB: str = "tourism"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
