import asyncio

from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from Domain.Entities.payment_outbox_message import PaymentOutboxMessage
from Domain.Repositories.payment_outbox_message_repository_interface import PaymentOutboxMessageRepositoryInterface

from .base_repository import BaseRepository

from ..Factories.payment_outbox_message_factory import PaymentOutboxMessageFactory
from ..Models.payment_outbox_message_orm import PaymentOutboxMessageORM
from ..Mappers.payment_outbox_message_mapper import PaymentOutboxMessageMapper


class PaymentOutboxMessageRepository(BaseRepository, PaymentOutboxMessageRepositoryInterface):
    _mapper : PaymentOutboxMessageMapper

    def __init__(self, session : AsyncSession):
        super().__init__(session = session)
        factory = PaymentOutboxMessageFactory()
        self._mapper = PaymentOutboxMessageMapper(factory = factory)

    async def add(self, entity : PaymentOutboxMessage) -> None:
        orm = await self._mapper.map_to_orm(entity)
        self._session.add(orm)

    async def get(self, entity_id : UUID) -> PaymentOutboxMessage:
        orm = await self._session.get(PaymentOutboxMessageORM, entity_id)
        if not orm:
            raise ValueError()
        return await self._mapper.map_to_entity(orm)

    async def get_unprocessed_messages(self, batch_size : int = 64) -> List[PaymentOutboxMessage]:
        query = select(PaymentOutboxMessageORM).where(PaymentOutboxMessageORM.processed == False).limit(batch_size)
        orm  = await self._session.execute(query)
        if not orm:
            raise ValueError()
        orm_orders = orm.scalars().all()
        orders = await asyncio.gather(*(self._mapper.map_to_entity(orm) for orm in orm_orders))
        return orders

    async def mark_as_processed(self, ids: List[UUID]) -> None:
        query = update(PaymentOutboxMessageORM).where(PaymentOutboxMessageORM.order_id.in_(ids)).values(processed = True)
        await self._session.execute(query)
