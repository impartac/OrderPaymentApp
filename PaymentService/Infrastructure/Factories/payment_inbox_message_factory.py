from datetime import datetime
from typing import Dict, Any

from Domain.Entities.payment_inbox_message import PaymentInboxMessage
from Domain.Factories.payment_inbox_message_factory_interface import PaymentInboxMessageFactoryInterface
from ..Models.payment_inbox_message_orm import PaymentInboxMessageORM


class PaymentInboxMessageFactory(PaymentInboxMessageFactoryInterface):

    async def build(self, obj : Dict[str, Any]) -> PaymentInboxMessage:
        return PaymentInboxMessage(
            order_id = obj["order_id"],
            user_id = obj["user_id"],
            amount = obj["amount"],
            processed = False,
            created_at = datetime.now()
        )
        
    async def create(self, obj : PaymentInboxMessageORM) -> PaymentInboxMessage:
        return PaymentInboxMessage(
            order_id = obj.order_id,
            user_id = obj.user_id,
            amount = obj.amount,
            processed = obj.processed,
            created_at = obj.created_at
        )
