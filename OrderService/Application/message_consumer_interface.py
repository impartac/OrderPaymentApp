from abc import ABC, abstractmethod


class MessageConsumerInterface(ABC):

    @abstractmethod
    async def consume_batch(self, batch_size : int = 64) -> None:
        pass
