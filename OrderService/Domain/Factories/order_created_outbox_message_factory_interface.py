from abc import ABC, abstractmethod

from ..Entities.order import Order
from ..Entities.order_created_outbox_message import OrderCreatedOutboxMessage
from .factory_interface import FactoryInterface

class OrderCreatedOutboxMessageFactoryInterface(FactoryInterface, ABC):
    
    @abstractmethod
    async def create(self, obj) -> OrderCreatedOutboxMessage:
        pass

    @abstractmethod
    async def build(self, order : Order) -> OrderCreatedOutboxMessage:
        pass
