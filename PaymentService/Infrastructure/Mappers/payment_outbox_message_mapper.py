from Domain.Entities.payment_outbox_message import PaymentOutboxMessage
from Domain.Factories.payment_outbox_message_factory_interface import PaymentOutboxMessageFactoryInterface

from ..Models.payment_outbox_message_orm import PaymentOutboxMessageORM


class PaymentOutboxMessageMapper:
    _factory : PaymentOutboxMessageFactoryInterface

    def __init__(self, factory : PaymentOutboxMessageFactoryInterface):
        self._factory = factory

    async def map_to_orm(self, entity : PaymentOutboxMessage) -> PaymentOutboxMessageORM:
        return PaymentOutboxMessageORM(
            order_id = entity.id,
            description = entity.description,
            is_success = entity.is_success,
            processed = entity.processed
        )
        
    async def map_to_entity(self, orm : PaymentOutboxMessageORM) -> PaymentOutboxMessage:
        return await self._factory.create(
            order_id = orm.order_id,
            is_success = orm.is_success,
            description = orm.description
        )
