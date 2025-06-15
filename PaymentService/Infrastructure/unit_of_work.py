from contextlib import asynccontextmanager
from typing import Optional
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from Domain.Repositories.payment_inbox_message_repository_interface import PaymentInboxMessageRepositoryInterface
from Domain.Repositories.bank_account_repostiroy_interface import BankAccountRepositoryInterface

from Application.unit_of_work_interface import UnitOfWorkInterface

from .Repositories.payment_inbox_message_repository import PaymentInboxMessageRepository
from .Repositories.payment_outbox_message_repository import PaymentOutboxMessageRepository
from .Repositories.bank_account_repository import BankAccountRepository


class UnitOfWork(UnitOfWorkInterface):

    _session_factory : async_sessionmaker
    _session : Optional[AsyncSession]
    _order_repository : Optional[BankAccountRepositoryInterface]
    _payment_outbox_message_repository: Optional[PaymentOutboxMessageRepository]
    _payment_inbox_message_repository : Optional[PaymentInboxMessageRepositoryInterface]

    def __init__(self, session_factory : async_sessionmaker):
        self._session_factory = session_factory
        self._session = None
        self._order_repository = None
        self._payment_outbox_message_repository = None
        self._payment_inbox_message_repository = None

    @asynccontextmanager
    async def start(self):
        self._session = self._session_factory()
        if not self._session:
            raise ValueError()
        try:
            yield self
            await self._session.commit()
        except Exception:
            await self._session.rollback()
            raise
        finally:
            await self._session.close()

    async def get_bank_account_repository(self) -> BankAccountRepository:
        if not self._session:
            raise ValueError()
        self._order_repository = BankAccountRepository(self._session)
        return self._order_repository

    async def get_payment_outbox_message_repository(self) -> PaymentOutboxMessageRepository:
        if not self._session:
            raise ValueError()
        self._payment_outbox_message_repository = PaymentOutboxMessageRepository(self._session)
        return self._payment_outbox_message_repository
    
    async def get_payment_inbox_message_repository(self) -> PaymentInboxMessageRepositoryInterface:
        if not self._session:
            raise ValueError()
        self._payment_inbox_message_repository = PaymentInboxMessageRepository(self._session)
        return self._payment_inbox_message_repository

    async def flush(self) -> None:
        if not self._session:
            raise ValueError()
        await self._session.flush()
