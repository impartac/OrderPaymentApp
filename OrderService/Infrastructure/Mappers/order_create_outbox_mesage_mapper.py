from Domain.Entities.order import Order
from Domain.Entities.order_created_outbox_message import OrderCreatedOutboxMessage
from Domain.Factories.order_created_outbox_message_factory_interface import OrderCreatedOutboxMessageFactoryInterface

from ..Models.order_created_outbox_message_orm import OrderCreatedOutboxMessageORM


class OrderCreateOutboxMessageMapper:
    _factory : OrderCreatedOutboxMessageFactoryInterface

    def __init__(self, factory : OrderCreatedOutboxMessageFactoryInterface):
        self._factory = factory

    async def map_to_entity(self, orm : OrderCreatedOutboxMessageORM) -> OrderCreatedOutboxMessage:
        return await self._factory.create(orm)

    async def map_to_orm(self, entity : OrderCreatedOutboxMessage) -> OrderCreatedOutboxMessageORM:
        return OrderCreatedOutboxMessageORM(
            order_id = entity.id,
            created_at = entity.created_at,
            processed = entity.processed,
            user_id = entity.user_id,
            amount = entity.amount
        )

    async def map_from_order(self, order : Order) -> OrderCreatedOutboxMessage:
        return await self._factory.build(order)
