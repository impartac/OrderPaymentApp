from abc import ABC, abstractmethod
from uuid import UUID

from Domain.Entities.order import Order
from .factory_interface import FactoryInterface

class OrderFactoryInterface(FactoryInterface, ABC):
    
    @abstractmethod
    async def create(self, obj) -> Order:
        pass
    
    @abstractmethod
    async def build(self, user_id : UUID,
                    amount : float,
                    description : str) -> Order:
        pass