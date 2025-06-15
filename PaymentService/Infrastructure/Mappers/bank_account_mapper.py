from Domain.Entities.bank_account import BankAccount
from Domain.Factories.bank_account_factory_interface import BankAccountFactoryInterface

from ..Models.bank_account_orm import BankAccountORM


class BankAccountMapper:
    _factory : BankAccountFactoryInterface

    def __init__(self, factory : BankAccountFactoryInterface):
        self._factory = factory

    async def map_to_entity(self, orm : BankAccountORM) -> BankAccount:
        return await self._factory.create(orm)

    async def map_to_orm(self, entity : BankAccount) -> BankAccountORM:
        return BankAccountORM(
            user_id = entity.id,
            balance = entity.balance,
            created_at = entity.created_at
        )
