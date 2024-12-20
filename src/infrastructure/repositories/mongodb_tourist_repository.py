from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson import ObjectId
from typing import Optional, List
from domain.repositories.tourist_repository import TouristRepositoryInterface
from domain.models.tourist import Tourist
from domain.models.preference import Preference

class MongoDBTouristRepository(TouristRepositoryInterface):
    def __init__(self, uri: str, database_name: str):
        """
        Initialize the MongoDB repository.
        :param uri: MongoDB connection URI.
        :param database_name: Name of the database to use.
        """
        self.client = MongoClient(uri)
        self.db = self.client[database_name]
        self.collection = self.db["tourists"]

    def save(self, tourist: Tourist) -> None:
        """
        Save or update a tourist in MongoDB.
        :param tourist: The tourist object to save.
        """
        tourist_data = {
            "name": tourist.name,
            "email": tourist.email,
            "preferences": vars(tourist.preferences) if tourist.preferences else None,
        }

        if tourist.id and ObjectId.is_valid(tourist.id):
            self.collection.update_one({"_id": ObjectId(tourist.id)}, {"$set": tourist_data}, upsert=True)
        else:
            result = self.collection.insert_one(tourist_data)
            tourist.id = str(result.inserted_id)

    def find_by_id(self, tourist_id: str) -> Optional[Tourist]:
        """
        Find a tourist by their ID.
        :param tourist_id: The ID of the tourist to find.
        :return: The tourist object, or None if not found.
        """
        try:
            # Attempt to convert and search for tourist by ObjectId
            if ObjectId.is_valid(tourist_id):
                data = self.collection.find_one({"_id": ObjectId(tourist_id)})
            else:
                data = None
        except PyMongoError as e:
            # Catch all MongoDB related exceptions
            print(f"Error finding tourist by ID: {e}")
            return None

        if not data:
            return None

        tourist = Tourist(name=data["name"], email=data["email"])
        tourist.id = str(data["_id"])

        if data.get("preferences"):
            preferences = Preference(**data["preferences"])
            tourist.set_preferences(preferences)

        return tourist

    def delete(self, tourist_id: str) -> bool:
        """
        Delete a tourist by their ID.
        :param tourist_id: The ID of the tourist to delete.
        :return: True if the tourist was deleted, False otherwise.
        """
        try:
            if ObjectId.is_valid(tourist_id):
                result = self.collection.delete_one({"_id": ObjectId(tourist_id)})
                return result.deleted_count > 0
            else:
                return False
        except PyMongoError as e:
            # Catch MongoDB related exceptions
            print(f"Error deleting tourist by ID: {e}")
            return False

    def list_all(self) -> List[Tourist]:
        """
        List all tourists in the MongoDB collection.
        :return: A list of all tourist objects.
        """
        tourists = []
        try:
            for data in self.collection.find():
                tourist = Tourist(name=data["name"], email=data["email"])
                tourist.id = str(data["_id"])

                if data.get("preferences"):
                    preferences = Preference(**data["preferences"])
                    tourist.set_preferences(preferences)

                tourists.append(tourist)
        except PyMongoError as e:
            # Handle MongoDB-related errors during fetching the list
            print(f"Error listing tourists: {e}")

        return tourists
