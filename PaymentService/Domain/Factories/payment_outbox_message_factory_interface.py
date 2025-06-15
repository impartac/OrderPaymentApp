from abc import ABC, abstractmethod
from uuid import UUID

from .factory_interface import FactoryInterface

from ..Entities.payment_outbox_message import PaymentOutboxMessage


class PaymentOutboxMessageFactoryInterface(FactoryInterface, ABC):
    
    @abstractmethod
    async def create_fail_message_by_account(self, order_id : UUID) -> PaymentOutboxMessage:
        pass
    
    @abstractmethod
    async def create_fail_message_by_balance(self, order_id : UUID) -> PaymentOutboxMessage:
        pass

    @abstractmethod
    async def create_success_message(self, order_id : UUID) -> PaymentOutboxMessage:
        pass
    
    @abstractmethod
    async def create(self, order_id: UUID, is_success : bool = False, description : str = str() ) -> PaymentOutboxMessage:
        pass