from typing import Dict, Any
from Domain.Entities.payment_inbox_message import PaymentInboxMessage
from Domain.Factories.payment_inbox_message_factory_interface import PaymentInboxMessageFactoryInterface

from ..Models.payment_inbox_message_orm import PaymentInboxMessageORM


class PaymentInboxMessageMapper:
    _factory : PaymentInboxMessageFactoryInterface

    def __init__(self, factory : PaymentInboxMessageFactoryInterface):
        self._factory = factory

    async def map_to_entity(self, orm : PaymentInboxMessageORM) -> PaymentInboxMessage:
        return await self._factory.create(orm)

    async def map_to_orm(self, entity : PaymentInboxMessage) -> PaymentInboxMessageORM:
        return PaymentInboxMessageORM(
            order_id = entity.id,
            created_at = entity.created_at,
            processed = entity.processed,
            user_id = entity.user_id,
            amount = entity.amount
        )

    async def map_from_dict(self, dictionary : Dict[str,Any]) -> PaymentInboxMessage:
        return await self._factory.build(dictionary)
