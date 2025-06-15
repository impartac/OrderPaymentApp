from typing import Dict, Any
from Domain.Entities.payment_processed_inbox_message import PaymentProcessedInboxMessage
from Domain.Factories.payment_processed_inbox_message_factory_interface import PaymentProcessedInboxMessageFactoryInterface

from ..Models.payment_processed_inbox_message_orm import PaymentProcessedInboxMessageORM


class PaymentProcessedInboxMessageMapper:
    _factory : PaymentProcessedInboxMessageFactoryInterface

    def __init__(self, factory : PaymentProcessedInboxMessageFactoryInterface):
        self._factory = factory

    async def map_to_entity(self, orm : PaymentProcessedInboxMessageORM) -> PaymentProcessedInboxMessage:
        return await self._factory.create(orm)

    async def map_to_orm(self, entity : PaymentProcessedInboxMessage) -> PaymentProcessedInboxMessageORM:
        return PaymentProcessedInboxMessageORM(
            order_id = entity.id,
            is_success = entity.is_success,
            processed = entity.processed,
            description = entity.description
        )

    async def map_from_dict(self, dictionary : Dict[str,Any]) -> PaymentProcessedInboxMessage:
        return await self._factory.build(dictionary)
