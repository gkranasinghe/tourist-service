import os
from pydantic_settings import BaseSettings
from pydantic import  ConfigDict

class AppConfig(BaseSettings):
    app_env: str = "development"  # Default to 'development' if not set
    database_type: str = "mongo"
    mongo_username: str
    mongo_password: str
    mongo_host: str = "localhost"
    mongo_port: int = 27017
    mongo_database: str 

    @property
    def mongo_uri(self) -> str:
        """Construct the MongoDB URI dynamically."""
        return f"mongodb://{self.mongo_username}:{self.mongo_password}@{self.mongo_host}:{self.mongo_port}"

    model_config = ConfigDict(env_file=f".env.{os.getenv('APP_ENV', 'development')}")

# Usage Example
config = AppConfig()  # This will read directly from environment variables
print("Config:", config)



