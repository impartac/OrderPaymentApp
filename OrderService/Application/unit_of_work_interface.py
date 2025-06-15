from abc import ABC, abstractmethod
from contextlib import asynccontextmanager

from Domain.Repositories.order_created_outbox_message_repository_interface import OrderCreatedOutboxMessageRepositoryInterface
from Domain.Repositories.order_repostiroy_interface import OrderRepositoryInterface
from Domain.Repositories.payment_processed_inbox_message_repository_interface import PaymentProcessedInboxMessageRepositoryInterface


class UnitOfWorkInterface(ABC):
    
    @abstractmethod
    async def get_order_repository(self) -> OrderRepositoryInterface:
        pass
    
    @abstractmethod
    async def get_order_created_outbox_message_repository(self) -> OrderCreatedOutboxMessageRepositoryInterface:
        pass
    
    @abstractmethod
    async def get_payment_processed_inbox_message_repository(self) -> PaymentProcessedInboxMessageRepositoryInterface:
        pass
    
    @abstractmethod
    async def flush(self) -> None:
        pass
    
    @asynccontextmanager
    @abstractmethod
    async def start(self):
        yield
