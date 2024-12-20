import pytest
from domain.models.tourist import Tourist, Preference
from infrastructure.repositories.mongodb_tourist_repository import MongoDBTouristRepository

@pytest.fixture
def test_repository():
    # Use a test MongoDB URI (e.g., MongoDB Atlas or a local test DB)
    repo = MongoDBTouristRepository(uri="mongodb://localhost:27017", database_name="test_db")
    repo.collection.delete_many({})  # Clear the test collection before each test
    return repo

def test_mongodb_tourist_repository(test_repository):
    repo = test_repository

    # Create and save a tourist
    tourist = Tourist(name="Alice", email="alice@example.com")
    preferences = Preference(travel_type="Adventure", nights=3, group_size=2)
    tourist.set_preferences(preferences)
    repo.save(tourist)

    # Test find_by_id
    found_tourist = repo.find_by_id(tourist.id)
    assert found_tourist is not None
    assert found_tourist.name == "Alice"

    # Test list_all
    tourists = repo.list_all()
    assert len(tourists) == 1

    # Test delete
    assert repo.delete(tourist.id) is True
    assert repo.find_by_id(tourist.id) is None
