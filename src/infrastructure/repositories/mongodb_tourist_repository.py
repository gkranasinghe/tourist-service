from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from domain.repositories.tourist_repository import TouristRepositoryInterface
from domain.models.tourist import Tourist
from infrastructure.config.config import AppConfig
from typing import Optional, List
import logging
from pydantic import ValidationError

# Configure logging for better error tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDBTouristRepository(TouristRepositoryInterface):
    _instance = None  # Singleton instance

    def __new__(cls, config: AppConfig):
        if cls._instance is None:
            try:
                cls._instance = super().__new__(cls)
                cls._instance.client = MongoClient(config.mongo_uri)
                cls._instance.db = cls._instance.client[config.mongo_database]
                cls._instance.collection = cls._instance.db["tourists"]
                logger.info(f"Connected to MongoDB database: {config.mongo_database}")
            except PyMongoError as e:
                logger.error(f"Failed to connect to MongoDB: {e}")
                raise ConnectionError(f"Unable to connect to MongoDB at {config.mongo_uri}")
        return cls._instance

    def close_connection(self):
        """Close the MongoDB connection."""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed.")

    def _to_mongo_document(self, tourist: Tourist) -> dict:
        """Convert Tourist domain model to MongoDB document."""
        document = tourist.model_dump()
        document['_id'] = ObjectId(tourist.id) if ObjectId.is_valid(tourist.id) else ObjectId()
        document['id'] = str(document['_id'])  # Store string ID for consistency
        return document

    def _from_mongo_document(self, document: dict) -> Optional[Tourist]:
        """Convert MongoDB document to Tourist domain model."""
        try:
            document['id'] = str(document['_id'])  # Convert ObjectId to string
            return Tourist(**document)
        except ValidationError as e:
            logger.error(f"Validation error converting document: {document}, error: {e}")
            return None

    def save(self, tourist: Tourist) -> Tourist:
        """Save or update a tourist in the database."""
        document = self._to_mongo_document(tourist)
        try:
            result = self.collection.replace_one(
                {"_id": document["_id"]}, document, upsert=True
            )
            if result.upserted_id:
                tourist.id = str(result.upserted_id)  # New document
                logger.info(f"New tourist created with ID {tourist.id}.")
            else:
                logger.info(f"Tourist with ID {tourist.id} updated.")
            return tourist
        except PyMongoError as e:
            logger.error(f"Error saving tourist: {e}")
            raise RuntimeError(f"Failed to save tourist: {e}")

    def find_by_id(self, tourist_id: str) -> Optional[Tourist]:
        """Find a tourist by their ID."""
        try:
            if not ObjectId.is_valid(tourist_id):
                logger.error(f"Invalid tourist ID: {tourist_id}")
                return None
            tourist_data = self.collection.find_one({"_id": ObjectId(tourist_id)})
            if tourist_data:
                logger.info(f"Tourist with ID {tourist_id} found.")
                return self._from_mongo_document(tourist_data)
            logger.warning(f"Tourist with ID {tourist_id} not found.")
            return None
        except PyMongoError as e:
            logger.error(f"Error retrieving tourist with ID {tourist_id}: {e}")
            raise RuntimeError(f"Failed to retrieve tourist with ID {tourist_id}")

    def delete(self, tourist_id: str) -> bool:
        """Delete a tourist by their ID."""
        try:
            if not ObjectId.is_valid(tourist_id):
                logger.error(f"Invalid tourist ID: {tourist_id}")
                return False
            result = self.collection.delete_one({"_id": ObjectId(tourist_id)})
            if result.deleted_count > 0:
                logger.info(f"Tourist with ID {tourist_id} deleted.")
                return True
            logger.warning(f"Tourist with ID {tourist_id} not found for deletion.")
            return False
        except PyMongoError as e:
            logger.error(f"Error deleting tourist with ID {tourist_id}: {e}")
            raise RuntimeError(f"Failed to delete tourist with ID {tourist_id}")

    def list_all(self) -> List[Tourist]:
        """List all tourists in the database."""
        try:
            cursor = self.collection.find()
            tourists = [self._from_mongo_document(doc) for doc in cursor]
            logger.info(f"Retrieved {len(tourists)} tourists from MongoDB.")
            return tourists
        except PyMongoError as e:
            logger.error(f"Error listing all tourists: {e}")
            raise RuntimeError("Failed to list all tourists")
