from abc import ABC, abstractmethod
from contextlib import asynccontextmanager

from Domain.Repositories.payment_inbox_message_repository_interface import PaymentInboxMessageRepositoryInterface
from Domain.Repositories.payment_outbox_message_repository_interface import PaymentOutboxMessageRepositoryInterface
from Domain.Repositories.bank_account_repostiroy_interface import BankAccountRepositoryInterface


class UnitOfWorkInterface(ABC):
    
    @abstractmethod
    async def get_bank_account_repository(self) -> BankAccountRepositoryInterface:
        pass
    
    @abstractmethod
    async def get_payment_outbox_message_repository(self) -> PaymentOutboxMessageRepositoryInterface:
        pass
    
    @abstractmethod
    async def get_payment_inbox_message_repository(self) -> PaymentInboxMessageRepositoryInterface:
        pass
    
    @asynccontextmanager
    @abstractmethod
    async def start(self):
        yield
