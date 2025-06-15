from abc import ABC, abstractmethod
from typing import List

from Domain.Entities.payment_processed_inbox_message import PaymentProcessedInboxMessage


class MessageConsumerInterface(ABC):

    @abstractmethod
    async def consume_batch(self, batch_size : int = 64) -> List[PaymentProcessedInboxMessage]:
        pass

    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass