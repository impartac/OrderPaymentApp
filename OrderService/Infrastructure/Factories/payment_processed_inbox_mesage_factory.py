from typing import Dict, Any

from Domain.Entities.payment_processed_inbox_message import PaymentProcessedInboxMessage
from Domain.Factories.payment_processed_inbox_message_factory_interface import PaymentProcessedInboxMessageFactoryInterface

from ..Models.payment_processed_inbox_message_orm import PaymentProcessedInboxMessageORM


class PaymentProcessedInboxMessageFactory(PaymentProcessedInboxMessageFactoryInterface):

    async def build(self, obj : Dict[str, Any]) -> PaymentProcessedInboxMessage:
        return PaymentProcessedInboxMessage(
            order_id = obj["order_id"],
            is_success = obj["is_success"],
            description = obj["description"],
            processed = False
        )
        
    async def create(self, obj : PaymentProcessedInboxMessageORM) -> PaymentProcessedInboxMessage:
        return PaymentProcessedInboxMessage(
            order_id = obj.order_id,
            is_success = obj.is_success,
            description = obj.description,
            processed = obj.processed,
        )
