class Preference:
    def __init__(self, travel_type: str, nights: int, group_size: int):
        self.travel_type = travel_type  # e.g., "ADVENTURE", "FAMILY"
        self.nights = nights
        self.group_size = group_size
