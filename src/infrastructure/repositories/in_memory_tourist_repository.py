import logging
from typing import Optional, List
from domain.repositories.tourist_repository import TouristRepositoryInterface
from domain.models.tourist import Tourist

# Configure logger for this module
logger = logging.getLogger(__name__)

class MemoryTouristRepository(TouristRepositoryInterface):
    _instance = None  # Class variable to hold the singleton instance

    def __new__(cls, *args, **kwargs):
        """
        Ensure only one instance of the repository exists.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.storage = {}  # Initialize storage on the first instance
            logger.info("Initialized MemoryTouristRepository with empty storage.")
        return cls._instance

    def save(self, tourist: Tourist) -> Tourist:
        """
        Save or update a tourist in the in-memory store.
        :param tourist: The tourist object to save.
        :return: The saved tourist with a valid ID.
        """
        if not tourist.id:
            tourist.id = str(len(self.storage) + 1)  # Simple unique ID generation
            logger.debug(f"Assigned new ID to tourist: {tourist.id}")
        else:
            logger.debug(f"Updating tourist with ID: {tourist.id}")
        
        self.storage[tourist.id] = tourist
        logger.info(f"Saved tourist with ID: {tourist.id}")
        return tourist

    def find_by_id(self, tourist_id: str) -> Optional[Tourist]:
        """
        Retrieve a tourist by their ID.
        :param tourist_id: The ID of the tourist to find.
        :return: The tourist object, or None if not found.
        """
        tourist = self.storage.get(tourist_id)
        if tourist:
            logger.info(f"Found tourist with ID: {tourist_id}")
        else:
            logger.warning(f"Tourist with ID {tourist_id} not found.")
        return tourist

    def delete(self, tourist_id: str) -> bool:
        """
        Delete a tourist by their ID.
        :param tourist_id: The ID of the tourist to delete.
        :return: True if the tourist was deleted, False otherwise.
        """
        if tourist_id in self.storage:
            del self.storage[tourist_id]
            logger.info(f"Deleted tourist with ID: {tourist_id}")
            return True
        logger.warning(f"Failed to delete tourist with ID: {tourist_id} - not found.")
        return False

    def list_all(self) -> List[Tourist]:
        """
        List all tourists in the in-memory store.
        :return: A list of all tourists.
        """
        logger.info(f"Listing all tourists. Total count: {len(self.storage)}")
        return list(self.storage.values())
