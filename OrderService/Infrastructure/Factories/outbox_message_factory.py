from Domain.Entities.order import Order
from Domain.Entities.outbox_message import OutboxMessage
from Domain.Factories.outbox_message_factory_interface import OutboxMessageFactoryInterface

from ..Models.outbox_message_orm import OutboxMessageORM


class OutboxMessageFactory(OutboxMessageFactoryInterface):

    async def create(self, obj : OutboxMessageORM) -> OutboxMessage:
        return OutboxMessage(
            order_id = obj.order_id,
            user_id = obj.user_id,
            amount = obj.amount,
            created_at = obj.created_at,
            processed = obj.processed
        )

    async def build(self, order : Order) -> OutboxMessage:
        return OutboxMessage(
            order_id = order.id,
            user_id = order.user_id,
            amount = order.amount
        )
