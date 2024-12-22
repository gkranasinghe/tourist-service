import pytest
from domain.models.tourist import Tourist
from domain.models.preference import Preference
from infrastructure.repositories.mongodb_tourist_repository import MongoDBTouristRepository
from infrastructure.config.config import AppConfig
from bson import ObjectId

@pytest.fixture(scope="module")
def test_config():
    return AppConfig(
        mongo_username="llm_engineering",
        mongo_password="llm_engineering",
        mongo_host="localhost",
        mongo_port=27017,
        mongo_database="test_db"
    )

@pytest.fixture(scope="module")
def test_repository(test_config):
    repo = MongoDBTouristRepository(config=test_config)
    repo.collection.delete_many({})  # Clear the test collection before the tests start
    yield repo
    repo.collection.delete_many({})  # Cleanup after tests complete




def test_save_find_list_delete_tourist(test_repository):
    repo = test_repository

    # Create and save a tourist
    tourist = Tourist(name="Alice", email="alice@example.com")
    preferences = Preference(travel_type="Adventure", nights=3, group_size=2)
    tourist.set_preferences(preferences)
    tourist = repo.save(tourist)

    # Ensure the tourist's ID is set
    assert ObjectId.is_valid(tourist.id)

    # Test find_by_id
    found_tourist = repo.find_by_id(tourist.id)  
    assert found_tourist is not None
    assert found_tourist.name == "Alice"
    assert found_tourist.preferences.travel_type == "Adventure"

    # Test list_all
    tourists = repo.list_all()  
    assert len(tourists) == 1
    assert tourists[0].name == "Alice"
    assert tourists[0].preferences.travel_type == "Adventure"

    # Test delete
    assert repo.delete(tourist.id) is True  
    found_tourist_after_deletion = repo.find_by_id(tourist.id)
    assert found_tourist_after_deletion is None

    # Test for ensuring the tourist is really deleted from the database
    tourists_after_deletion = repo.list_all()  
    assert len(tourists_after_deletion) == 0

def test_mongo_singleton():
    # Ensure Singleton pattern works by checking if two instances of the repo are the same
    repo1 = MongoDBTouristRepository(config=test_config)
    repo2 = MongoDBTouristRepository(config=test_config)

    # Both repositories should be the same instance
    assert repo1 is repo2
