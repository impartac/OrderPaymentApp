import asyncio

from uuid import UUID
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from Domain.Repositories.order_repostiroy_interface import OrderRepositoryInterface
from Domain.Entities.order import Order
from Domain.Enums.status_enum import STATUS

from .base_repository import BaseRepository

from ..Models.order_orm import OrderORM
from ..Factories.order_factory import OrderFactory
from ..Mappers.order_mapper import OrderMapper

class OrderRepository(BaseRepository, OrderRepositoryInterface):
    _mapper : OrderMapper

    def __init__(self, session : AsyncSession):
        super().__init__(session = session)
        factory = OrderFactory()
        self._mapper = OrderMapper(factory = factory)

    async def add(self, entity : Order) -> None:
        orm = await self._mapper.map_to_orm(entity)
        self._session.add(orm)

    async def get(self, entity_id : UUID) -> Order:
        orm = await self._session.get(OrderORM, entity_id)
        if not orm:
            raise ValueError()
        return await self._mapper.map_to_entity(orm)

    async def get_list(self, user_id : UUID) -> List[Order]:
        query = select(OrderORM).where(OrderORM.user_id == user_id)
        response = await self._session.execute(query)
        if not response:
            raise ValueError()
        orm_orders = response.scalars()
        orders = await asyncio.gather(*(self._mapper.map_to_entity(orm) for orm in orm_orders))
        return orders

    async def get_status(self, order_id : UUID) -> STATUS:
        orm = await self._session.get(OrderORM, order_id)
        if not orm:
            raise ValueError()
        return orm.status
