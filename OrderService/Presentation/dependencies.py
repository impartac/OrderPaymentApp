from fastapi import Depends
from sqlalchemy.ext.asyncio import  async_sessionmaker

from Domain.Factories.order_factory_interface import OrderFactoryInterface
from Domain.Factories.order_created_outbox_message_factory_interface import OrderCreatedOutboxMessageFactoryInterface

from Infrastructure.Config.config import session_maker
from Infrastructure.Factories.order_created_outbox_message_factory import OrderCreatedOutboxMessageFactory
from Infrastructure.Factories.order_factory import OrderFactory
from Infrastructure.Mappers.order_mapper import OrderMapper
from Infrastructure.Mappers.order_create_outbox_mesage_mapper import OrderCreateOutboxMessageMapper
from Infrastructure.unit_of_work import UnitOfWork

from Application.mappers import DTOOrderMapper, DTOOrderCreatedOutboxMessageMapper
from Application.UseCases.create_order_use_case import CreateOrderUseCase
from Application.unit_of_work_interface import UnitOfWorkInterface
from Application.UseCases.order_status_use_case import OrderStatusUseCase
from Application.UseCases.order_list_use_case import OrderListUseCase


async def get_session_factory() -> async_sessionmaker:
    return session_maker

async def get_order_factory() -> OrderFactory:
    return OrderFactory()

async def get_outbox_message_factory() -> OrderCreatedOutboxMessageFactory:
    return OrderCreatedOutboxMessageFactory()

async def get_order_mapper(
    factory : OrderFactoryInterface = Depends(get_order_factory)
) -> OrderMapper:
    return OrderMapper(factory = factory)

async def get_outbox_message_mapper(
    factory : OrderCreatedOutboxMessageFactoryInterface = Depends(get_outbox_message_factory)
) -> OrderCreateOutboxMessageMapper:
    return OrderCreateOutboxMessageMapper(factory = factory)

async def get_dto_order_mapper(
    factory : OrderFactoryInterface = Depends(get_order_factory)
) -> DTOOrderMapper:
    return DTOOrderMapper(factory = factory)

async def get_dto_outbox_message_mapper(
    factory : OrderCreatedOutboxMessageFactoryInterface = Depends(get_outbox_message_factory)
) -> DTOOrderCreatedOutboxMessageMapper:
    return DTOOrderCreatedOutboxMessageMapper(factory = factory)

async def get_unit_of_work(
    session_factory : async_sessionmaker = Depends(get_session_factory)
) -> UnitOfWork:
    return UnitOfWork(session_factory = session_factory)

async def get_create_order_use_case(
    uow : UnitOfWorkInterface = Depends(get_unit_of_work),
    dto_order_mapper : DTOOrderMapper = Depends(get_dto_order_mapper),
    dto_order_created_outbox_message_mapper : DTOOrderCreatedOutboxMessageMapper = Depends(get_dto_outbox_message_mapper)
) -> CreateOrderUseCase:
    return CreateOrderUseCase(
        uow = uow,
        dto_order_mapper = dto_order_mapper,
        dto_order_created_outbox_message_mapper = dto_order_created_outbox_message_mapper
    )

async def get_order_list_use_case(
    uow : UnitOfWorkInterface = Depends(get_unit_of_work)
) -> OrderListUseCase:
    return OrderListUseCase(uow = uow)

async def get_order_status_use_case(
    uow : UnitOfWorkInterface = Depends(get_unit_of_work)
) -> OrderStatusUseCase:
    return OrderStatusUseCase(uow = uow)
