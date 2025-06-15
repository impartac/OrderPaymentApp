from uuid import UUID
from Domain.Entities.payment_outbox_message import PaymentOutboxMessage
from Domain.Factories.payment_outbox_message_factory_interface import PaymentOutboxMessageFactoryInterface


class PaymentOutboxMessageFactory(PaymentOutboxMessageFactoryInterface):

    async def create_fail_message_by_account(self, order_id : UUID) -> PaymentOutboxMessage:
        return PaymentOutboxMessage(
            order_id = order_id,
            is_success = False,
            description = "Account doesn't exist",
            processed = False 
        )

    async def create_fail_message_by_balance(self, order_id : UUID) -> PaymentOutboxMessage:
        return PaymentOutboxMessage(
            order_id = order_id,
            is_success = False,
            description = "Not enough balance",
            processed = False
        )

    async def create_success_message(self, order_id : UUID) -> PaymentOutboxMessage:
        return PaymentOutboxMessage(
            order_id = order_id,
            is_success = True,
            description = str(),
            processed = False
        )

    async def create(self, order_id: UUID, is_success : bool = False, description : str = str(), processed : bool = False ) -> PaymentOutboxMessage:
        return PaymentOutboxMessage(
            order_id = order_id,
            is_success = is_success,
            description = description,
            processed = processed
        )