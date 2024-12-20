from fastapi import Depends
from domain.repositories.tourist_repository import TouristRepositoryInterface
from infrastructure.repositories.in_memory_tourist_repository import MemoryTouristRepository
from infrastructure.repositories.mongodb_tourist_repository import MongoDBTouristRepository
from application.services.tourist_service import TouristService
from .settings import Settings, get_settings

# Cache to store singleton instances
repository_cache = None
tourist_service_cache = None

def get_repository(settings: Settings = Depends(get_settings)) -> TouristRepositoryInterface:
    global repository_cache
    if repository_cache is None:
        if settings.USE_MONGODB:
            repository_cache = MongoDBTouristRepository(
                uri=settings.MONGODB_URI,
                database_name=settings.MONGODB_DB
            )
        else:
            repository_cache = MemoryTouristRepository()
    return repository_cache

def get_tourist_service(
    repository: TouristRepositoryInterface = Depends(get_repository)
) -> TouristService:
    global tourist_service_cache
    if tourist_service_cache is None:
        tourist_service_cache = TouristService(repository=repository)
    return tourist_service_cache
