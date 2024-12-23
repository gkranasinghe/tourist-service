import pytest
from domain.models.tourist import Tourist
from domain.models.preference import Preference
from infrastructure.repositories.mongodb_tourist_repository import MongoDBTouristRepository
from infrastructure.repositories.in_memory_tourist_repository import MemoryTouristRepository
from infrastructure.config.config import AppConfig
from bson import ObjectId
from unittest.mock import patch


# Configuring database types via pytest fixtures or environment variables
@pytest.fixture(scope="module")
def test_config():
    return AppConfig(
        database_type="mongo",
        mongo_username="llm_engineering",
        mongo_password="llm_engineering",
        mongo_host="localhost",
        mongo_port=27017,
        mongo_database="test_db"
    )

# Fixture to switch between MongoDB and In-memory repositories
@pytest.fixture(scope="module")
def test_repository(test_config):
    if test_config.database_type == "mongo":
        repo = MongoDBTouristRepository(config=test_config)
        repo.collection.delete_many({})  # Clear the test collection before the tests start
        yield repo
        repo.collection.delete_many({})  # Cleanup after tests complete
    else:
        repo = MemoryTouristRepository()
        yield repo  # In-memory repository does not require cleanup

# Parametrize tests to work with both MongoDB and In-memory repositories
@pytest.mark.parametrize("test_repository", [MongoDBTouristRepository, MemoryTouristRepository], indirect=True)
def test_save_tourist(test_repository):
    repo = test_repository

    # Create and save a tourist
    tourist = Tourist(name="Alice", email="alice@example.com")
    preferences = Preference(travel_type="Adventure", nights=3, group_size=2)
    tourist.set_preferences(preferences)
    saved_tourist = repo.save(tourist)

    # Ensure the tourist's ID is set, checking for MongoDB or in-memory
    if isinstance(repo, MongoDBTouristRepository):
        assert ObjectId.is_valid(saved_tourist.id)
    else:
        assert saved_tourist.id is not None

def test_find_by_id(test_repository):
    repo = test_repository

    # Create and save a tourist
    tourist = Tourist(name="Alice", email="alice@example.com")
    preferences = Preference(travel_type="Adventure", nights=3, group_size=2)
    tourist.set_preferences(preferences)
    saved_tourist = repo.save(tourist)

    # Test find_by_id
    found_tourist = repo.find_by_id(saved_tourist.id)
    assert found_tourist is not None
    assert found_tourist.name == "Alice"
    assert found_tourist.preferences.travel_type == "Adventure"

def test_list_all_tourists(test_repository):
    repo = test_repository

    # Get the initial number of tourists in the database
    initial_count = len(repo.list_all())

    # Create and save tourists
    tourist1 = Tourist(name="Alice", email="alice@example.com")
    preferences1 = Preference(travel_type="Adventure", nights=3, group_size=2)
    tourist1.set_preferences(preferences1)
    repo.save(tourist1)

    tourist2 = Tourist(name="Bob", email="bob@example.com")
    preferences2 = Preference(travel_type="Relaxation", nights=5, group_size=1)
    tourist2.set_preferences(preferences2)
    repo.save(tourist2)

    # Get the updated number of tourists
    updated_count = len(repo.list_all())

    # Check if the number of tourists increased by 2
    assert updated_count == initial_count + 2

    # Optionally, you can check the names of the newly added tourists
    tourists = repo.list_all()
    assert tourists[-2].name == "Alice"
    assert tourists[-1].name == "Bob"

def test_delete_tourist(test_repository):
    repo = test_repository

    # Create and save a tourist
    tourist = Tourist(name="Alice", email="alice@example.com")
    preferences = Preference(travel_type="Adventure", nights=3, group_size=2)
    tourist.set_preferences(preferences)
    saved_tourist = repo.save(tourist)

    # Test delete
    delete_result = repo.delete(saved_tourist.id)
    assert delete_result is True

    # Ensure the tourist is deleted
    found_tourist = repo.find_by_id(saved_tourist.id)
    assert found_tourist is None

def test_invalid_tourist_id(test_repository):
    repo = test_repository

    # Test invalid tourist ID in find_by_id
    invalid_id = "12345"  # Invalid ObjectId
    tourist = repo.find_by_id(invalid_id)
    assert tourist is None  # Expecting None for invalid ID

    # Test invalid tourist ID in delete
    delete_result = repo.delete(invalid_id)
    assert not delete_result  # Expecting False for invalid ID

def test_upsert_tourist(test_repository):
    repo = test_repository

    # Create and save a tourist
    tourist = Tourist(name="Alice", email="alice@example.com")
    preferences = Preference(travel_type="Adventure", nights=3, group_size=2)
    tourist.set_preferences(preferences)
    tourist = repo.save(tourist)

    # Save again with new data to test upsert
    tourist.name = "Alice Updated"
    tourist.preferences.travel_type = "Relaxation"
    updated_tourist = repo.save(tourist)

    # Ensure the tourist was updated
    found_tourist = repo.find_by_id(tourist.id)
    assert found_tourist.name == "Alice Updated"
    assert found_tourist.preferences.travel_type == "Relaxation"


def test_database_connection_error():
    with patch("infrastructure.repositories.mongodb_tourist_repository.MongoDBTouristRepository.__new__") as mock_new:
        mock_new.side_effect = ConnectionError("Unable to connect to MongoDB")
        try:
            repo = MongoDBTouristRepository(config=AppConfig())
        except ConnectionError as e:
            assert str(e) == "Unable to connect to MongoDB"

def test_repo_singleton(test_config):
    # Depending on the test config, we either use the MongoDB or the Memory repository
    if test_config.database_type == "mongo":
        # Test MongoDB repository
        repo1 = MongoDBTouristRepository(config=test_config)
        repo2 = MongoDBTouristRepository(config=test_config)
        assert repo1 is repo2  # Ensures singleton behavior
    else:
        # Test in-memory repository
        repo1 = MemoryTouristRepository()
        repo2 = MemoryTouristRepository()
        assert repo1 is repo2  # Ensures singleton behavior
