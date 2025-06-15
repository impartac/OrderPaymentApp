from abc import abstractmethod
from uuid import UUID
from typing import List

from Domain.Entities.order_created_outbox_message import OrderCreatedOutboxMessage
from .repository_interface import RepositoryInterface

class OrderCreatedOutboxMessageRepositoryInterface(RepositoryInterface):

    @abstractmethod
    async def add(self, entity : OrderCreatedOutboxMessage) -> UUID:
        pass

    @abstractmethod   
    async def get(self, entity_id : UUID) -> OrderCreatedOutboxMessage:
        pass

    @abstractmethod
    async def get_unprocessed_messages(self, batch_size: int = 64) -> List[OrderCreatedOutboxMessage]:
        pass

    @abstractmethod
    async def mark_as_processed(self, ids : List[UUID]) -> None:
        pass
