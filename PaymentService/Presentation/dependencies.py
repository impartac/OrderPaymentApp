from fastapi import Depends
from sqlalchemy.ext.asyncio import  async_sessionmaker

from Domain.Factories.bank_account_factory_interface import BankAccountFactoryInterface
from Domain.Factories.payment_outbox_message_factory_interface import PaymentOutboxMessageFactoryInterface
from Domain.Factories.payment_inbox_message_factory_interface import PaymentInboxMessageFactoryInterface

from Infrastructure.Config.config import session_maker
from Infrastructure.Factories.payment_inbox_message_factory import PaymentInboxMessageFactory
from Infrastructure.Factories.payment_outbox_message_factory import PaymentOutboxMessageFactory
from Infrastructure.Factories.bank_account_factory import BankAccountFactory
from Infrastructure.Mappers.bank_account_mapper import BankAccountMapper
from Infrastructure.Mappers.payment_inbox_message_mapper import PaymentInboxMessageMapper
from Infrastructure.Mappers.payment_outbox_message_mapper import PaymentOutboxMessageMapper
from Infrastructure.unit_of_work import UnitOfWork

from Application.mappers import DTOBankAccountMapper, DTOPaymnetInboxMessageMapper
from Application.UseCases.create_bank_account_use_case import CreateBankAccountUseCase
from Application.unit_of_work_interface import UnitOfWorkInterface
from Application.UseCases.bank_account_balance_use_case import BankAccountBalanceUseCase
from Application.UseCases.replenish_balance_use_case import ReplenishBalanceUseCase


async def get_session_factory() -> async_sessionmaker:
    return session_maker

async def get_bank_account_factory() -> BankAccountFactory:
    return BankAccountFactory()

async def get_payment_inbox_message_factory() -> PaymentInboxMessageFactory:
    return PaymentInboxMessageFactory()

async def get_payment_outbox_message_factory() -> PaymentOutboxMessageFactory:
    return PaymentOutboxMessageFactory()

async def get_bank_account_mapper(
    factory : BankAccountFactoryInterface = Depends(get_bank_account_factory)
) -> BankAccountMapper:
    return BankAccountMapper(factory = factory)

async def get_payment_inbox_message_mapper(
    factory : PaymentInboxMessageFactoryInterface = Depends(get_payment_inbox_message_factory)
) -> PaymentInboxMessageMapper:
    return PaymentInboxMessageMapper(factory = factory)

async def get_dto_bank_account_mapper(
    factory : BankAccountFactoryInterface = Depends(get_bank_account_factory)
) -> DTOBankAccountMapper:
    return DTOBankAccountMapper(factory = factory)

async def get_dto_payment_inbox_message_mapper(
    factory : PaymentInboxMessageFactoryInterface = Depends(get_payment_inbox_message_factory)
) -> DTOPaymnetInboxMessageMapper:
    return DTOPaymnetInboxMessageMapper(factory = factory)

async def get_unit_of_work(
    session_factory : async_sessionmaker = Depends(get_session_factory)
) -> UnitOfWork:
    return UnitOfWork(session_factory = session_factory)

async def get_create_bank_account_use_case(
    uow : UnitOfWorkInterface = Depends(get_unit_of_work),
    dto_bank_account_mapper : DTOBankAccountMapper = Depends(get_dto_bank_account_mapper)
) -> CreateBankAccountUseCase:
    return CreateBankAccountUseCase(
        uow = uow,
        dto_bank_account_mapper = dto_bank_account_mapper
    )

async def get_replenish_balance_use_case(
    uow : UnitOfWorkInterface = Depends(get_unit_of_work)
) -> ReplenishBalanceUseCase:
    return ReplenishBalanceUseCase(uow = uow)

async def get_bank_account_balance_use_case(
    uow : UnitOfWorkInterface = Depends(get_unit_of_work)
) -> BankAccountBalanceUseCase:
    return BankAccountBalanceUseCase(uow = uow)
