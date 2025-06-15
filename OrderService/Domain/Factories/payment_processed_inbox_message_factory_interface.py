from abc import ABC, abstractmethod
from typing import Dict, Any

from .factory_interface import FactoryInterface

from ..Entities.payment_processed_inbox_message import PaymentProcessedInboxMessage


class PaymentProcessedInboxMessageFactoryInterface(FactoryInterface, ABC):
    
    @abstractmethod
    async def create(self, obj : Any) -> PaymentProcessedInboxMessage:
        pass

    @abstractmethod
    async def build(self, obj : Dict[str, Any]) -> PaymentProcessedInboxMessage:
        pass
