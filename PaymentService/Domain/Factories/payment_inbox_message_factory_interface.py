from abc import ABC, abstractmethod
from typing import Dict, Any

from .factory_interface import FactoryInterface

from ..Entities.payment_inbox_message import PaymentInboxMessage


class PaymentInboxMessageFactoryInterface(FactoryInterface, ABC):
    
    @abstractmethod
    async def create(self, obj : Any) -> PaymentInboxMessage:
        pass

    @abstractmethod
    async def build(self, obj : Dict[str, Any]) -> PaymentInboxMessage:
        pass
