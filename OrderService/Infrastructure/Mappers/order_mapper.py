
from Domain.Entities.order import Order
from Domain.Factories.order_factory_interface import OrderFactoryInterface

from ..Models.order_orm import OrderORM


class OrderMapper:
    _factory : OrderFactoryInterface

    def __init__(self, factory : OrderFactoryInterface):
        self._factory = factory
        
    async def map_to_entity(self, orm : OrderORM) -> Order:
        return await self._factory.create(orm)

    async def map_to_orm(self, entity : Order) -> OrderORM:
        return OrderORM(
            id = entity.id,
            user_id = entity.user_id,
            amount = entity.amount,
            description = entity.description,
            status = entity.status
        )
