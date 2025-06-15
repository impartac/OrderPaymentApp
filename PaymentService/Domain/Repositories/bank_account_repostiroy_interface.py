from abc import abstractmethod
from uuid import UUID

from Domain.Entities.bank_account import BankAccount
from .repository_interface import RepositoryInterface

class BankAccountRepositoryInterface(RepositoryInterface):

    @abstractmethod
    async def add(self, entity : BankAccount) -> UUID:
        pass
    @abstractmethod
    async def get(self, entity_id : UUID) -> BankAccount:
        pass
    
    @abstractmethod
    async def get_balance(self, user_id : UUID) -> float:
        pass
    
    @abstractmethod
    async def replenish_balance(self, user_id : UUID, amount : float) -> float:
        pass
