from abc import ABC
from uuid import UUID

class Entity(ABC):
    id : UUID

    def __init__(self, entity_id : UUID):
        self.id = entity_id
