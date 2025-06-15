from Domain.Entities.order_created_outbox_message import OrderCreatedOutboxMessage
from Domain.Factories.order_factory_interface import OrderFactoryInterface
from Domain.Entities.order import Order
from Domain.Factories.order_created_outbox_message_factory_interface import OrderCreatedOutboxMessageFactoryInterface
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

class DTOOrderCreatedOutboxMessageMapper:
    _factory : OrderCreatedOutboxMessageFactoryInterface

    def __init__(self, factory : OrderCreatedOutboxMessageFactoryInterface):
        self._factory = factory

    async def map_from_order(self, order : Order) -> OrderCreatedOutboxMessage:
        return await self._factory.build(order)
