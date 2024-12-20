from typing import Optional, List, Dict
from domain.repositories.tourist_repository import TouristRepositoryInterface
from domain.models.tourist import Tourist

class MemoryTouristRepository(TouristRepositoryInterface):
    def __init__(self):
        """
        Initialize the in-memory repository with a simple dictionary.
        """
        self.storage: Dict[str, Tourist] = {}

    def save(self, tourist: Tourist) -> None:
        """
        Save or update a tourist in the in-memory store.
        :param tourist: The tourist object to save.
        """
        self.storage[tourist.id] = tourist

    def find_by_id(self, tourist_id: str) -> Optional[Tourist]:
        """
        Retrieve a tourist by their ID.
        :param tourist_id: The ID of the tourist to find.
        :return: The tourist object, or None if not found.
        """
        return self.storage.get(tourist_id)

    def delete(self, tourist_id: str) -> bool:
        """
        Delete a tourist by their ID.
        :param tourist_id: The ID of the tourist to delete.
        :return: True if the tourist was deleted, False otherwise.
        """
        if tourist_id in self.storage:
            del self.storage[tourist_id]
            return True
        return False

    def list_all(self) -> List[Tourist]:
        """
        List all tourists in the in-memory store.
        :return: A list of all tourists.
        """
        return list(self.storage.values())