from uuid import uuid4

class Tourist:
    def __init__(self, name: str, email: str, tourist_id: str = None):
        self.id = tourist_id if tourist_id else str(uuid4())
        self.name = name
        self.email = email
        self.preferences = None  # Will be assigned a Preference object later

    def set_preferences(self, preferences):
        self.preferences = preferences
