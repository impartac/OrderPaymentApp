from abc import abstractmethod
from uuid import UUID
from typing import List

from .repository_interface import RepositoryInterface

from ..Entities.payment_outbox_message import PaymentOutboxMessage

class PaymentOutboxMessageRepositoryInterface(RepositoryInterface):

    @abstractmethod
    async def add(self, entity : PaymentOutboxMessage) -> UUID:
        pass

    @abstractmethod   
    async def get(self, entity_id : UUID) -> PaymentOutboxMessage:
        pass

    @abstractmethod
    async def get_unprocessed_messages(self, batch_size: int = 64) -> List[PaymentOutboxMessage]:
        pass

    @abstractmethod
    async def mark_as_processed(self, ids : List[UUID]) -> None:
        pass
