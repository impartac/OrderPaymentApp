from abc import abstractmethod
from uuid import UUID
from typing import List

from .repository_interface import RepositoryInterface

from ..Entities.payment_processed_inbox_message import PaymentProcessedInboxMessage

class PaymentProcessedInboxMessageRepositoryInterface(RepositoryInterface):

    @abstractmethod
    async def add(self, entity : PaymentProcessedInboxMessage) -> UUID:
        pass

    @abstractmethod   
    async def get(self, entity_id : UUID) -> PaymentProcessedInboxMessage:
        pass

    @abstractmethod
    async def get_unprocessed_messages(self, batch_size: int = 64) -> List[PaymentProcessedInboxMessage]:
        pass

    @abstractmethod
    async def mark_as_processed(self, ids : List[UUID]) -> None:
        pass
