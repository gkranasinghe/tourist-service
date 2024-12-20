from fastapi import APIRouter, HTTPException, Depends
from application.services.tourist_service import TouristService
from application.schemas.tourist import CreateTouristRequest ,UpdatePreferencesRequest
from domain.repositories.tourist_repository import TouristRepositoryInterface
from infrastructure.repositories.in_memory_tourist_repository import MemoryTouristRepository
from infrastructure.repositories.mongodb_tourist_repository import MongoDBTouristRepository

# Dependency Injection for Repository
def get_repository() -> TouristRepositoryInterface:
    # Replace with MongoDB repository if required
    # return MongoDBTouristRepository(uri="mongodb://localhost:27017", database_name="tourism")
    return MemoryTouristRepository()

# Dependency Injection for Service
def get_tourist_service(repository: TouristRepositoryInterface = Depends(get_repository)) -> TouristService:
    return TouristService(repository=repository)

# Use a router for modularity
router = APIRouter()

@router.post("/")
def create_tourist(request: CreateTouristRequest, service: TouristService = Depends(get_tourist_service)):
    tourist = service.create_tourist(request.name, request.email)
    return {"id": tourist.id, "name": tourist.name, "email": tourist.email}


@router.put("/{tourist_id}/preferences")
def update_preferences(
    tourist_id: str,
    travel_type: str,
    nights: int,
    group_size: int,
    service: TouristService = Depends(get_tourist_service),
):
    try:
        tourist = service.update_preferences(tourist_id, travel_type, nights, group_size)
        return {"id": tourist.id, "preferences": tourist.preferences.__dict__}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/")
def list_tourists(service: TouristService = Depends(get_tourist_service)):
    tourists = service.list_tourists()
    return [
        {"id": tourist.id, "name": tourist.name, "email": tourist.email, "preferences": vars(tourist.preferences) if tourist.preferences else None}
        for tourist in tourists
    ]

@router.get("/{tourist_id}")
def get_tourist(tourist_id: str, service: TouristService = Depends(get_tourist_service)):
    try:
        tourist = service.get_tourist_by_id(tourist_id)
        return {
            "id": tourist.id,
            "name": tourist.name,
            "email": tourist.email,
            "preferences": vars(tourist.preferences) if tourist.preferences else None,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{tourist_id}")
def delete_tourist(tourist_id: str, service: TouristService = Depends(get_tourist_service)):
    deleted = service.delete_tourist(tourist_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tourist not found")
    return {"message": "Tourist deleted successfully"}
