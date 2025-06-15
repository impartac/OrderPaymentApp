from uuid import UUID
from Domain.Entities.bank_account import BankAccount
from Domain.Factories.bank_account_factory_interface import BankAccountFactoryInterface

from ..Models.bank_account_orm import BankAccountORM

class BankAccountFactory(BankAccountFactoryInterface):

    async def create(self, obj : BankAccountORM) -> BankAccount:
        return BankAccount(
            user_id = obj.user_id,
            balance = obj.balance,
            created_at = obj.created_at 
        )

    async def build(self, user_id : UUID) -> BankAccount:
        return BankAccount(
            user_id = user_id
        )
