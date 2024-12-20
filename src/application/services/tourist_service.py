from domain.models.tourist import Tourist
from domain.models.preference import Preference
from domain.repositories.tourist_repository import TouristRepositoryInterface

class TouristService:
    def __init__(self, repository: TouristRepositoryInterface):
        """
        Initialize the TouristService with a repository instance.
        :param repository: An implementation of TouristRepositoryInterface.
        """
        self.repository = repository

    def create_tourist(self, name: str, email: str) -> Tourist:
        """
        Create a new tourist and save them to the repository.
        :param name: The name of the tourist.
        :param email: The email of the tourist.
        :return: The created Tourist object.
        """
        tourist = Tourist(name=name, email=email)
        self.repository.save(tourist)
        return tourist

    def update_preferences(self, tourist_id: str, travel_type: str, nights: int, group_size: int) -> Tourist:
        """
        Update the preferences of an existing tourist.
        :param tourist_id: The ID of the tourist.
        :param travel_type: Travel type (e.g., Adventure, Family).
        :param nights: Number of nights.
        :param group_size: Size of the travel group.
        :return: The updated Tourist object.
        :raises ValueError: If the tourist is not found.
        """
        tourist = self.repository.find_by_id(tourist_id)
        if not tourist:
            raise ValueError("Tourist not found")

        preferences = Preference(travel_type, nights, group_size)
        tourist.set_preferences(preferences)
        self.repository.save(tourist)
        return tourist

    def delete_tourist(self, tourist_id: str) -> bool:
        """
        Delete a tourist by their ID.
        :param tourist_id: The ID of the tourist to delete.
        :return: True if the tourist was deleted, False otherwise.
        """
        return self.repository.delete(tourist_id)

    def list_tourists(self) -> list[Tourist]:
        """
        List all tourists from the repository.
        :return: A list of Tourist objects.
        """
        return self.repository.list_all()

    def get_tourist_by_id(self, tourist_id: str) -> Tourist:
        """
        Retrieve a tourist by their ID.
        :param tourist_id: The ID of the tourist to retrieve.
        :return: The Tourist object if found.
        :raises ValueError: If the tourist is not found.
        """
        tourist = self.repository.find_by_id(tourist_id)
        if not tourist:
            raise ValueError("Tourist not found")
        return tourist
