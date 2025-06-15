import asyncio

from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from Domain.Entities.order_created_outbox_message import OrderCreatedOutboxMessage
from Domain.Repositories.order_created_outbox_message_repository_interface import OrderCreatedOutboxMessageRepositoryInterface

from .base_repository import BaseRepository

from ..Factories.order_created_outbox_message_factory import OrderCreatedOutboxMessageFactory
from ..Models.order_created_outbox_message_orm import OrderCreatedOutboxMessageORM
from ..Mappers.order_create_outbox_mesage_mapper import OrderCreateOutboxMessageMapper


class OrderCreatedOutboxMessageRepository(BaseRepository, OrderCreatedOutboxMessageRepositoryInterface):
    _mapper : OrderCreateOutboxMessageMapper

    def __init__(self, session : AsyncSession):
        super().__init__(session = session)
        factory = OrderCreatedOutboxMessageFactory()
        self._mapper = OrderCreateOutboxMessageMapper(factory = factory)

    async def add(self, entity : OrderCreatedOutboxMessage) -> None:
        orm = await self._mapper.map_to_orm(entity)
        self._session.add(orm)

    async def get(self, entity_id : UUID) -> OrderCreatedOutboxMessage:
        orm = await self._session.get(OrderCreatedOutboxMessageORM, entity_id)
        if not orm:
            raise ValueError()
        return await self._mapper.map_to_entity(orm)

    async def get_unprocessed_messages(self, batch_size : int = 64) -> List[OrderCreatedOutboxMessage]:
        query = select(OrderCreatedOutboxMessageORM).where(OrderCreatedOutboxMessageORM.processed == False).limit(batch_size)
        orm  = await self._session.execute(query)
        if not orm:
            raise ValueError()
        orm_orders = orm.scalars().all()
        orders = await asyncio.gather(*(self._mapper.map_to_entity(orm) for orm in orm_orders))
        return orders

    async def mark_as_processed(self, ids: List[UUID]) -> None:
        query = update(OrderCreatedOutboxMessageORM).where(OrderCreatedOutboxMessageORM.order_id.in_(ids)).values(processed = True)
        await self._session.execute(query)
