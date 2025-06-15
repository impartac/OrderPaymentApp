from abc import ABC, abstractmethod
from typing import List

from Domain.Entities.payment_inbox_message import PaymentInboxMessage


class MessageConsumerInterface(ABC):

    @abstractmethod
    async def consume_batch(self, batch_size : int = 64) -> List[PaymentInboxMessage]:
        pass

    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass