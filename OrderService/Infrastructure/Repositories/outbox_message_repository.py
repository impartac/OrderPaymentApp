import asyncio

from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from Domain.Entities.outbox_message import OutboxMessage
from Domain.Repositories.outbox_message_repository_interface import OutboxMessageRepositoryInterface

from .base_repository import BaseRepository

from ..Factories.outbox_message_factory import OutboxMessageFactory
from ..Models.outbox_message_orm import OutboxMessageORM
from ..Mappers.outbox_mesage_mapper import OutboxMessageMapper


class OutboxMessageRepository(BaseRepository, OutboxMessageRepositoryInterface):
    _mapper : OutboxMessageMapper

    def __init__(self, session : AsyncSession):
        super().__init__(session = session)
        factory = OutboxMessageFactory()
        self._mapper = OutboxMessageMapper(factory = factory)

    async def add(self, entity : OutboxMessage) -> None:
        orm = await self._mapper.map_to_orm(entity)
        self._session.add(orm)

    async def get(self, entity_id : UUID) -> OutboxMessage:
        orm = await self._session.get(OutboxMessageORM, entity_id)
        if not orm:
            raise ValueError()
        return await self._mapper.map_to_entity(orm)

    async def get_unprocessed_messages(self, batch_size : int = 64) -> List[OutboxMessage]:
        query = select(OutboxMessageORM).where(OutboxMessageORM.processed == False).limit(batch_size)
        orm  = await self._session.execute(query)
        if not orm:
            raise ValueError()
        orm_orders = orm.scalars().all()
        orders = await asyncio.gather(*(self._mapper.map_to_entity(orm) for orm in orm_orders))
        return orders

    async def mark_as_processed(self, ids: List[UUID]) -> None:
        query = update(OutboxMessageORM).where(OutboxMessageORM.order_id.in_(ids)).values(processed = True)
        await self._session.execute(query)
