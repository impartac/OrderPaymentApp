from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from Domain.Entities.order_created_outbox_message import OrderCreatedOutboxMessage


class MessageProducerInterface(ABC):

    @abstractmethod
    async def send_message_batch(self, messages : List[OrderCreatedOutboxMessage]) -> List[UUID]:
        pass
    
    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass