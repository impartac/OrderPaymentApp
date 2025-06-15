# from Domain.Entities.payment_inbox_message import PaymentInboxMessage
from Domain.Factories.bank_account_factory_interface import BankAccountFactoryInterface
from Domain.Entities.bank_account import BankAccount
from Domain.Factories.payment_inbox_message_factory_interface import PaymentInboxMessageFactoryInterface
from .dto import CreateBankAccountDTO


class DTOBankAccountMapper:
    _factory: BankAccountFactoryInterface

    def __init__(self, factory : BankAccountFactoryInterface):
        self._factory = factory

    async def map_from_dto(self, dto : CreateBankAccountDTO) -> BankAccount:
        return await self._factory.build(
            user_id = dto.user_id,
        )

class DTOPaymnetInboxMessageMapper:
    _factory : PaymentInboxMessageFactoryInterface

    def __init__(self, factory : PaymentInboxMessageFactoryInterface):
        self._factory = factory

    # async def map_from_order(self, order : BankAccount) -> OutboxMessage:
    #     return await self._factory.build(order)
