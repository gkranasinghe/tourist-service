from fastapi import Depends
from domain.repositories.tourist_repository import TouristRepositoryInterface
from infrastructure.repositories.in_memory_tourist_repository import MemoryTouristRepository
from infrastructure.repositories.mongodb_tourist_repository import MongoDBTouristRepository
from application.services.tourist_service import TouristService
from .config import AppConfig

# Cache to store singleton instances
repository_cache = None
tourist_service_cache = None

# Initialize the configuration globally
config = AppConfig()  # Reads environment variables once

class RepositoryFactory:
    @staticmethod
    def create_repository() -> TouristRepositoryInterface:
        """
        Factory method to create the appropriate repository implementation.
        """
        if config.database_type == "mongo":
            return MongoDBTouristRepository(config)
        return MemoryTouristRepository()

def get_repository() -> TouristRepositoryInterface:
    global repository_cache
    if repository_cache is None:
        repository_cache = RepositoryFactory.create_repository()
    return repository_cache

def get_tourist_service(
    repository: TouristRepositoryInterface = Depends(get_repository)
) -> TouristService:
    global tourist_service_cache
    if tourist_service_cache is None:
        tourist_service_cache = TouristService(repository=repository)
    return tourist_service_cache

def shutdown_repository():
    """
    Clean up resources used by repositories.
    """
    global repository_cache
    if repository_cache and isinstance(repository_cache, MongoDBTouristRepository):
        repository_cache.close_connection()
