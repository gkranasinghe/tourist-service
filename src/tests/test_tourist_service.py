import pytest
from domain.models.tourist import Tourist
from domain.models.preference import Preference
from infrastructure.repositories.mongodb_tourist_repository import MongoDBTouristRepository
from bson import ObjectId


@pytest.fixture(scope="module")
def test_repository():
    # Use a test MongoDB URI (e.g., MongoDB Atlas or a local test DB)
    # The 'scope="module"' ensures that the test repository is created only once per test module
    repo = MongoDBTouristRepository(uri="mongodb://localhost:27017", database_name="test_db")
    repo.collection.delete_many({})  # Clear the test collection before the tests start
    yield repo
    repo.collection.delete_many({})  # Cleanup after tests complete

def test_mongodb_tourist_repository(test_repository):
    repo = test_repository

    # Create and save a tourist
    tourist = Tourist(name="Alice", email="alice@example.com")
    preferences = Preference(travel_type="Adventure", nights=3, group_size=2)
    tourist.set_preferences(preferences)
    repo.save(tourist)

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
    assert repo.find_by_id(tourist.id) is None

    # Test for ensuring the tourist is really deleted from the database
    tourists_after_deletion = repo.list_all()
    assert len(tourists_after_deletion) == 0

def test_mongo_singleton(test_repository):
    # Ensure Singleton pattern works by checking if two instances of the repo are the same
    repo1 = MongoDBTouristRepository(uri="mongodb://localhost:27017", database_name="test_db")
    repo2 = MongoDBTouristRepository(uri="mongodb://localhost:27017", database_name="test_db")

    # Both repositories should be the same instance
    assert repo1 is repo2
