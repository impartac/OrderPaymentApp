from abc import ABC, abstractmethod
from contextlib import asynccontextmanager

from Domain.Repositories.outbox_message_repository_interface import OutboxMessageRepositoryInterface
from Domain.Repositories.order_repostiroy_interface import OrderRepositoryInterface


class UnitOfWorkInterface(ABC):
    
    @abstractmethod
    async def get_order_repository(self) -> OrderRepositoryInterface:
        pass
    
    @abstractmethod
    async def get_outbox_message_repository(self) -> OutboxMessageRepositoryInterface:
        pass
    
    @asynccontextmanager
    @abstractmethod
    async def start(self):
        yield
