from uuid import UUID, uuid4
from Domain.Entities.order import Order
from Domain.Enums.status_enum import STATUS
from Domain.Factories.order_factory_interface import OrderFactoryInterface

from ..Models.order_orm import OrderORM

class OrderFactory(OrderFactoryInterface):

    async def create(self, obj : OrderORM) -> Order:
        return Order(
            entity_id = obj.id,
            user_id = obj.user_id,
            amount = obj.amount,
            description = obj.description,
            status = obj.status
        )
    
    async def build(self, user_id : UUID,
                    amount : float,
                    description : str) -> Order:
        return Order(
            entity_id = uuid4(),
            user_id=user_id,
            amount=amount,
            description=description,
            status=STATUS.NEW
        )