from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from Domain.Entities.payment_outbox_message import PaymentOutboxMessage


class MessageProducerInterface(ABC):

    @abstractmethod
    async def send_message_batch(self, messages : List[PaymentOutboxMessage]) -> List[UUID]:
        pass
    
    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass