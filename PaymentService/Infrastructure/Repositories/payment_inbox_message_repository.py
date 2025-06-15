import asyncio

from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from Domain.Entities.payment_inbox_message import PaymentInboxMessage
from Domain.Repositories.payment_inbox_message_repository_interface import PaymentInboxMessageRepositoryInterface

from .base_repository import BaseRepository

from ..Factories.payment_inbox_message_factory import PaymentInboxMessageFactory
from ..Models.payment_inbox_message_orm import PaymentInboxMessageORM
from ..Mappers.payment_inbox_message_mapper import PaymentInboxMessageMapper


class PaymentInboxMessageRepository(BaseRepository, PaymentInboxMessageRepositoryInterface):
    _mapper : PaymentInboxMessageMapper

    def __init__(self, session : AsyncSession):
        super().__init__(session = session)
        factory = PaymentInboxMessageFactory()
        self._mapper = PaymentInboxMessageMapper(factory = factory)

    async def add(self, entity : PaymentInboxMessage) -> None:
        orm = await self._mapper.map_to_orm(entity)
        self._session.add(orm)

    async def get(self, entity_id : UUID) -> PaymentInboxMessage:
        orm = await self._session.get(PaymentInboxMessageORM, entity_id)
        if not orm:
            raise ValueError()
        return await self._mapper.map_to_entity(orm)

    async def get_unprocessed_messages(self, batch_size : int = 64) -> List[PaymentInboxMessage]:
        query = select(PaymentInboxMessageORM).where(PaymentInboxMessageORM.processed == False).limit(batch_size)
        orm  = await self._session.execute(query)
        if not orm:
            raise ValueError()
        orm_orders = orm.scalars().all()
        orders = await asyncio.gather(*(self._mapper.map_to_entity(orm) for orm in orm_orders))
        return orders

    async def mark_as_processed(self, ids: List[UUID]) -> None:
        query = update(PaymentInboxMessageORM).where(PaymentInboxMessageORM.order_id.in_(ids)).values(processed = True)
        await self._session.execute(query)
