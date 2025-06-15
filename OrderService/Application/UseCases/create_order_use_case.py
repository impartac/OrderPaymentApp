from logging import getLogger

from Domain.Entities.order import Order

from ..unit_of_work_interface import UnitOfWorkInterface
from ..dto import CreateOrderDTO
from ..mappers import DTOOrderMapper, DTOOrderCreatedOutboxMessageMapper

logger = getLogger(__name__)

class CreateOrderUseCase:
    _uow : UnitOfWorkInterface
    _dto_order_mapper : DTOOrderMapper
    _dto_order_created_outbox_message_mapper : DTOOrderCreatedOutboxMessageMapper

    def __init__(self, uow : UnitOfWorkInterface,
                dto_order_mapper : DTOOrderMapper,
                dto_order_created_outbox_message_mapper : DTOOrderCreatedOutboxMessageMapper):
        self._uow = uow
        self._dto_order_mapper = dto_order_mapper
        self._dto_order_created_outbox_message_mapper = dto_order_created_outbox_message_mapper

    async def perfom(self, order_create_dto : CreateOrderDTO) -> Order:
        order = await self._dto_order_mapper.map_from_dto(order_create_dto)
        logger.info(f"ORDER ##############\n\n\n\n\n{order_create_dto.__dict__}")
        logger.info(f"ORDER ##############\n\n\n\n\n{order.__dict__}")
        outbox_message = await self._dto_order_created_outbox_message_mapper.map_from_order(order)
        async with self._uow.start():
            _order_repository = await self._uow.get_order_repository()
            _order_created_outbox_message_repository = await self._uow.get_order_created_outbox_message_repository()
            await _order_repository.add(order)
            await self._uow.flush()
            await _order_created_outbox_message_repository.add(outbox_message)
            return order
    