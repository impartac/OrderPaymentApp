from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from Domain.Entities.outbox_message import OutboxMessage


class MessageProducerInterface(ABC):

    @abstractmethod
    async def send_message_batch(self, messages : List[OutboxMessage]) -> List[UUID]:
        pass
