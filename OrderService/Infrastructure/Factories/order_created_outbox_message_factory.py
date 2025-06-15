from Domain.Entities.order import Order
from Domain.Entities.order_created_outbox_message import OrderCreatedOutboxMessage
from Domain.Factories.order_created_outbox_message_factory_interface import OrderCreatedOutboxMessageFactoryInterface

from ..Models.order_created_outbox_message_orm import OrderCreatedOutboxMessageORM


class OrderCreatedOutboxMessageFactory(OrderCreatedOutboxMessageFactoryInterface):

    async def create(self, obj : OrderCreatedOutboxMessageORM) -> OrderCreatedOutboxMessage:
        return OrderCreatedOutboxMessage(
            order_id = obj.order_id,
            user_id = obj.user_id,
            amount = obj.amount,
            created_at = obj.created_at,
            processed = obj.processed
        )

    async def build(self, order : Order) -> OrderCreatedOutboxMessage:
        return OrderCreatedOutboxMessage(
            order_id = order.id,
            user_id = order.user_id,
            amount = order.amount
        )
