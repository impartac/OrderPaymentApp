from Domain.Entities.outbox_message import OutboxMessage
from Domain.Factories.order_factory_interface import OrderFactoryInterface
from Domain.Entities.order import Order
from Domain.Factories.outbox_message_factory_interface import OutboxMessageFactoryInterface
from .dto import CreateOrderDTO


class DTOOrderMapper:
    _factory: OrderFactoryInterface

    def __init__(self, factory : OrderFactoryInterface):
        self._factory = factory
      
    async def map_from_dto(self, dto : CreateOrderDTO) -> Order:
        return await self._factory.build(
            user_id = dto.user_id,
            amount = dto.amount,
            description= dto.description
        )

class DTOOutboxMessageMapper:
    _factory : OutboxMessageFactoryInterface

    def __init__(self, factory : OutboxMessageFactoryInterface):
        self._factory = factory

    async def map_from_order(self, order : Order) -> OutboxMessage:
        return await self._factory.build(order)
