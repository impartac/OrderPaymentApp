from uuid import UUID

from Domain.Enums.status_enum import STATUS

from ..unit_of_work_interface import UnitOfWorkInterface


class OrderStatusUseCase:
    _uow : UnitOfWorkInterface

    def __init__(self, uow : UnitOfWorkInterface):
        self._uow = uow

    async def perform(self, order_id : UUID) -> STATUS:
        async with self._uow.start():
            order_repository = await self._uow.get_order_repository()
            return await order_repository.get_status(order_id = order_id)
