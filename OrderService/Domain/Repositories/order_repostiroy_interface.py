from abc import abstractmethod
from uuid import UUID
from typing import List

from Domain.Entities.order import Order
from ..Enums.status_enum import STATUS
from .repository_interface import RepositoryInterface

class OrderRepositoryInterface(RepositoryInterface):

    @abstractmethod
    async def add(self, entity : Order) -> UUID:
        pass
    @abstractmethod
    async def get(self, entity_id : UUID) -> Order:
        pass
    
    @abstractmethod
    async def get_list(self, user_id : UUID) -> List[Order]:
        pass
    
    @abstractmethod
    async def get_status(self, order_id : UUID) -> STATUS:
        pass
