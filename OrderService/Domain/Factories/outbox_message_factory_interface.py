from abc import ABC, abstractmethod

from ..Entities.order import Order
from ..Entities.outbox_message import OutboxMessage
from .factory_interface import FactoryInterface

class OutboxMessageFactoryInterface(FactoryInterface, ABC):
    
    @abstractmethod
    async def create(self, obj) -> OutboxMessage:
        pass

    @abstractmethod
    async def build(self, order : Order) -> OutboxMessage:
        pass
