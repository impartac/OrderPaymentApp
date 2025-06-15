from abc import abstractmethod
from uuid import UUID
from typing import List

from Domain.Entities.outbox_message import OutboxMessage
from .repository_interface import RepositoryInterface

class OutboxMessageRepositoryInterface(RepositoryInterface):

    @abstractmethod
    async def add(self, entity : OutboxMessage) -> UUID:
        pass

    @abstractmethod   
    async def get(self, entity_id : UUID) -> OutboxMessage:
        pass

    @abstractmethod
    async def get_unprocessed_messages(self, batch_size: int = 64) -> List[OutboxMessage]:
        pass

    @abstractmethod
    async def mark_as_processed(self, ids : List[UUID]) -> None:
        pass
