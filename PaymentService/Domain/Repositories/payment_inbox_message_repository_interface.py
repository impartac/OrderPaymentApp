from abc import abstractmethod
from uuid import UUID
from typing import List

from .repository_interface import RepositoryInterface

from ..Entities.payment_inbox_message import PaymentInboxMessage

class PaymentInboxMessageRepositoryInterface(RepositoryInterface):

    @abstractmethod
    async def add(self, entity : PaymentInboxMessage) -> UUID:
        pass

    @abstractmethod   
    async def get(self, entity_id : UUID) -> PaymentInboxMessage:
        pass

    @abstractmethod
    async def get_unprocessed_messages(self, batch_size: int = 64) -> List[PaymentInboxMessage]:
        pass

    @abstractmethod
    async def mark_as_processed(self, ids : List[UUID]) -> None:
        pass
