from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    app_env: str = "development"  # Default to 'development' if not set
    database_type: str = "mongo"
    mongo_username: str
    mongo_password: str
    mongo_host: str = "localhost"
    mongo_port: int = 27017
    mongo_database: str = "travel_db"
    in_memory_enabled: bool = False

    @property
    def mongo_uri(self) -> str:
        """Construct the MongoDB URI dynamically."""
        return f"mongodb://{self.mongo_username}:{self.mongo_password}@{self.mongo_host}:{self.mongo_port}"

    class Config:
        env_file = ".env"  # Optional: Can be used for local dev only (non-sensitive)

# Usage Example
config = AppConfig()  # This will read directly from environment variables
print("MongoDB URI:", config.mongo_uri)



