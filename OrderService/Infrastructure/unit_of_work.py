from contextlib import asynccontextmanager
from typing import Optional
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from Domain.Repositories.payment_processed_inbox_message_repository_interface import PaymentProcessedInboxMessageRepositoryInterface
from Domain.Repositories.order_created_outbox_message_repository_interface import OrderCreatedOutboxMessageRepositoryInterface
from Domain.Repositories.order_repostiroy_interface import OrderRepositoryInterface

from .Repositories.order_created_outbox_message_repository import OrderCreatedOutboxMessageRepository
from .Repositories.order_repository import OrderRepository
from .Repositories.payment_processed_inbox_message_repository import PaymentProcessedInboxMessageRepository

from Application.unit_of_work_interface import UnitOfWorkInterface


class UnitOfWork(UnitOfWorkInterface):

    _session_factory : async_sessionmaker
    _session : Optional[AsyncSession]
    _order_repository : Optional[OrderRepositoryInterface]
    _order_created_outbox_message_repository: Optional[OrderCreatedOutboxMessageRepositoryInterface]
    _payment_processed_inbox_message_repository : Optional[PaymentProcessedInboxMessageRepositoryInterface]

    def __init__(self, session_factory : async_sessionmaker):
        self._session_factory = session_factory
        self._session = None
        self._order_repository = None
        self._order_created_outbox_message_repository = None
        self._payment_processed_inbox_message_repository = None

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

    async def get_order_repository(self) -> OrderRepository:
        if not self._session:
            raise ValueError()
        self._order_repository = OrderRepository(self._session)
        return self._order_repository

    async def get_order_created_outbox_message_repository(self) -> OrderCreatedOutboxMessageRepository:
        if not self._session:
            raise ValueError()
        self._order_created_outbox_message_repository = OrderCreatedOutboxMessageRepository(self._session)
        return self._order_created_outbox_message_repository
    
    async def get_payment_processed_inbox_message_repository(self) -> PaymentProcessedInboxMessageRepository:
        if not self._session:
            raise ValueError()
        self._payment_processed_inbox_message_repository = PaymentProcessedInboxMessageRepository(self._session)
        return self._payment_processed_inbox_message_repository

    async def flush(self) -> None:
        if not self._session:
            raise ValueError()
        await self._session.flush()