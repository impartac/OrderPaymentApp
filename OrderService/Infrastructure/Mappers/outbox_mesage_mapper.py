from Domain.Entities.order import Order
from Domain.Entities.outbox_message import OutboxMessage
from Domain.Factories.outbox_message_factory_interface import OutboxMessageFactoryInterface

from ..Models.outbox_message_orm import OutboxMessageORM


class OutboxMessageMapper:
    _factory : OutboxMessageFactoryInterface

    def __init__(self, factory : OutboxMessageFactoryInterface):
        self._factory = factory

    async def map_to_entity(self, orm : OutboxMessageORM) -> OutboxMessage:
        return await self._factory.create(orm)

    async def map_to_orm(self, entity : OutboxMessage) -> OutboxMessageORM:
        return OutboxMessageORM(
            order_id = entity.id,
            created_at = entity.created_at,
            processed = entity.processed,
            user_id = entity.user_id,
            amount = entity.amount
        )

    async def map_from_order(self, order : Order) -> OutboxMessage:
        return await self._factory.build(order)
