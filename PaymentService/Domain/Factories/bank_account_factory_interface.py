from abc import ABC, abstractmethod
from uuid import UUID

from Domain.Entities.bank_account import BankAccount
from .factory_interface import FactoryInterface

class BankAccountFactoryInterface(FactoryInterface, ABC):
    
    @abstractmethod
    async def create(self, obj) -> BankAccount:
        pass
    
    @abstractmethod
    async def build(self, user_id : UUID) -> BankAccount:
        pass