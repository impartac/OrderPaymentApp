from contextlib import asynccontextmanager
from typing import Optional
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from Domain.Repositories.outbox_message_repository_interface import OutboxMessageRepositoryInterface
from Domain.Repositories.order_repostiroy_interface import OrderRepositoryInterface

from .Repositories.outbox_message_repository import OutboxMessageRepository
from .Repositories.order_repository import OrderRepository

from Application.unit_of_work_interface import UnitOfWorkInterface


class UnitOfWork(UnitOfWorkInterface):

    _session_factory : async_sessionmaker
    _session : Optional[AsyncSession]
    _order_repository : Optional[OrderRepositoryInterface]
    _outbox_message_repository: Optional[OutboxMessageRepositoryInterface]

    def __init__(self, session_factory : async_sessionmaker):
        self._session_factory = session_factory
        self._session = None
        self._order_repository = None
        self._outbox_message_repository = None

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

    async def get_outbox_message_repository(self) -> OutboxMessageRepository:
        if not self._session:
            raise ValueError()
        self._outbox_message_repository = OutboxMessageRepository(self._session)
        return self._outbox_message_repository
