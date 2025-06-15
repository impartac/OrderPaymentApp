from abc import ABC, abstractmethod
from uuid import UUID

from Domain.Entities.entity import Entity

class RepositoryInterface(ABC):

    @abstractmethod
    async def add(self, entity : Entity) -> None:
        pass

    @abstractmethod   
    async def get(self, entity_id : UUID) -> Entity:
        pass
    