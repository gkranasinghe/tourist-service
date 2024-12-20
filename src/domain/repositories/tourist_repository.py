from abc import ABC, abstractmethod
from typing import Optional, List
from domain.models.tourist import Tourist

class TouristRepositoryInterface(ABC):
    @abstractmethod
    def save(self, tourist: Tourist) -> None:
        """
        Save or update a tourist in the repository.
        :param tourist: The tourist object to save.
        """
        pass

    @abstractmethod
    def find_by_id(self, tourist_id: str) -> Optional[Tourist]:
        """
        Find a tourist by their ID.
        :param tourist_id: The ID of the tourist to find.
        :return: The tourist object, or None if not found.
        """
        pass

    @abstractmethod
    def delete(self, tourist_id: str) -> bool:
        """
        Delete a tourist by their ID.
        :param tourist_id: The ID of the tourist to delete.
        :return: True if the tourist was deleted, False otherwise.
        """
        pass

    @abstractmethod
    def list_all(self) -> List[Tourist]:
        """
        List all tourists in the repository.
        :return: A list of all tourists.
        """
        pass
