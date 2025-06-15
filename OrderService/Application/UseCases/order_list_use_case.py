from uuid import UUID
from typing import List

from Domain.Entities.order import Order

from ..unit_of_work_interface import UnitOfWorkInterface


class OrderListUseCase:
    _uow : UnitOfWorkInterface

    def __init__(self, uow : UnitOfWorkInterface):
        self._uow = uow

    async def perform(self, user_id : UUID) -> List[Order]:
        async with self._uow.start():
            order_repository = await self._uow.get_order_repository()
            return await order_repository.get_list(user_id = user_id)
