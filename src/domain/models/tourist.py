# Tourist model with Pydantic (simple and domain-focused)
from pydantic import BaseModel
from uuid import uuid4
from typing import Optional
from domain.models.preference import Preference

class Tourist(BaseModel):
    id: str
    name: str
    email: str
    preferences: Optional[Preference] = None

    def __init__(self, **kwargs):
        if not kwargs.get("id"):
            kwargs["id"] = str(uuid4())
        super().__init__(**kwargs)

    def set_preferences(self, preferences: Preference):
        self.preferences = preferences
