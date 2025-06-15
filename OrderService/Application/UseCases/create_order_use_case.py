from Domain.Entities.order import Order

from ..unit_of_work_interface import UnitOfWorkInterface
from ..dto import CreateOrderDTO
from ..mappers import DTOOrderMapper, DTOOutboxMessageMapper


class CreateOrderUseCase:
    _uow : UnitOfWorkInterface
    _dto_order_mapper : DTOOrderMapper
    _dto_outbox_message_mapper : DTOOutboxMessageMapper

    def __init__(self, uow : UnitOfWorkInterface,
                dto_order_mapper : DTOOrderMapper,
                dto_outbox_message_mapper : DTOOutboxMessageMapper):
        self._uow = uow
        self._dto_order_mapper = dto_order_mapper
        self._dto_outbox_message_mapper = dto_outbox_message_mapper

    async def perfom(self, order_create_dto : CreateOrderDTO) -> Order:
        order = await self._dto_order_mapper.map_from_dto(order_create_dto)
        outbox_message = await self._dto_outbox_message_mapper.map_from_order(order)
        async with self._uow.start():
            _order_repository = await self._uow.get_order_repository()
            _outbox_message_repository = await self._uow.get_outbox_message_repository()
            await _order_repository.add(order)
            await _outbox_message_repository.add(outbox_message)
            return order
    