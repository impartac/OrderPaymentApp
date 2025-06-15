import asyncio

from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from Domain.Entities.payment_processed_inbox_message import PaymentProcessedInboxMessage
from Domain.Repositories.payment_processed_inbox_message_repository_interface import PaymentProcessedInboxMessageRepositoryInterface

from .base_repository import BaseRepository

from ..Factories.payment_processed_inbox_mesage_factory import PaymentProcessedInboxMessageFactory
from ..Models.payment_processed_inbox_message_orm import PaymentProcessedInboxMessageORM
from ..Mappers.payment_processed_inbox_message_mapper import PaymentProcessedInboxMessageMapper


class PaymentProcessedInboxMessageRepository(BaseRepository, PaymentProcessedInboxMessageRepositoryInterface):
    _mapper : PaymentProcessedInboxMessageMapper

    def __init__(self, session : AsyncSession):
        super().__init__(session = session)
        factory = PaymentProcessedInboxMessageFactory()
        self._mapper = PaymentProcessedInboxMessageMapper(factory = factory)

    async def add(self, entity : PaymentProcessedInboxMessage) -> None:
        orm = await self._mapper.map_to_orm(entity)
        self._session.add(orm)

    async def get(self, entity_id : UUID) -> PaymentProcessedInboxMessage:
        orm = await self._session.get(PaymentProcessedInboxMessageORM, entity_id)
        if not orm:
            raise ValueError()
        return await self._mapper.map_to_entity(orm)

    async def get_unprocessed_messages(self, batch_size : int = 64) -> List[PaymentProcessedInboxMessage]:
        query = select(PaymentProcessedInboxMessageORM).where(PaymentProcessedInboxMessageORM.processed == False).limit(batch_size)
        orm  = await self._session.execute(query)
        if not orm:
            raise ValueError()
        orm_orders = orm.scalars().all()
        orders = await asyncio.gather(*(self._mapper.map_to_entity(orm) for orm in orm_orders))
        return orders

    async def mark_as_processed(self, ids: List[UUID]) -> None:
        query = update(PaymentProcessedInboxMessageORM).where(PaymentProcessedInboxMessageORM.order_id.in_(ids)).values(processed = True)
        await self._session.execute(query)
