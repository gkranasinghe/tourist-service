from pymongo import MongoClient
from pymongo.errors import PyMongoError
from domain.repositories.tourist_repository import TouristRepositoryInterface
from domain.models.tourist import Tourist
from typing import Optional, List
import logging
from uuid import uuid4

# Configure logging for better error tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDBTouristRepository(TouristRepositoryInterface):
    _instance = None  # Singleton instance

    def __new__(cls, uri: str, database_name: str):
        if cls._instance is None:
            try:
                cls._instance = super().__new__(cls)
                cls._instance.client = MongoClient(uri)
                cls._instance.db = cls._instance.client[database_name]
                cls._instance.collection = cls._instance.db["tourists"]
                logger.info(f"Connected to MongoDB database: {database_name}")
            except PyMongoError as e:
                logger.error(f"Failed to connect to MongoDB: {e}")
                raise ConnectionError(f"Unable to connect to MongoDB at {uri}")
        return cls._instance

    def save(self, tourist: Tourist) -> None:
        try:
            # Convert Tourist to dictionary, ensure '_id' is properly handled
            tourist_dict = tourist.dict(exclude_unset=True)
            tourist_dict["_id"] = tourist.id  # Ensure the UUID is set as the '_id'
            self.collection.replace_one(
                {"_id": tourist.id},
                tourist_dict,
                upsert=True
            )
            logger.info(f"Tourist with ID {tourist.id} saved/updated.")
        except PyMongoError as e:
            logger.error(f"Error saving tourist with ID {tourist.id}: {e}")
            raise Exception(f"Failed to save tourist with ID {tourist.id}")

    def find_by_id(self, tourist_id: str) -> Optional[Tourist]:
        try:
            tourist_data = self.collection.find_one({"_id": tourist_id})
            if tourist_data:
                logger.info(f"Tourist with ID {tourist_id} found.")
                return Tourist(**tourist_data)  # Use Pydantic to handle deserialization
            else:
                logger.warning(f"Tourist with ID {tourist_id} not found.")
                return None
        except PyMongoError as e:
            logger.error(f"Error retrieving tourist with ID {tourist_id}: {e}")
            raise Exception(f"Failed to retrieve tourist with ID {tourist_id}")

    def delete(self, tourist_id: str) -> bool:
        try:
            result = self.collection.delete_one({"_id": tourist_id})
            if result.deleted_count > 0:
                logger.info(f"Tourist with ID {tourist_id} deleted.")
                return True
            else:
                logger.warning(f"Tourist with ID {tourist_id} not found for deletion.")
                return False
        except PyMongoError as e:
            logger.error(f"Error deleting tourist with ID {tourist_id}: {e}")
            raise Exception(f"Failed to delete tourist with ID {tourist_id}")

    def list_all(self) -> List[Tourist]:
        try:
            tourists = [Tourist(**doc) for doc in self.collection.find()]
            logger.info(f"Retrieved {len(tourists)} tourists from MongoDB.")
            return tourists
        except PyMongoError as e:
            logger.error(f"Error listing all tourists: {e}")
            raise Exception("Failed to list all tourists")
