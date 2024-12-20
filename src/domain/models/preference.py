# Tourist model with Pydantic (simple and domain-focused)
from pydantic import BaseModel


class Preference(BaseModel):
    travel_type: str
    nights: int
    group_size: int