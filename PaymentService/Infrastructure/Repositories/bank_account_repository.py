from uuid import UUID

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from Domain.Repositories.bank_account_repostiroy_interface import BankAccountRepositoryInterface
from Domain.Entities.bank_account import BankAccount

from .base_repository import BaseRepository

from ..Models.bank_account_orm import BankAccountORM
from ..Factories.bank_account_factory import BankAccountFactory
from ..Mappers.bank_account_mapper import BankAccountMapper

class BankAccountRepository(BaseRepository, BankAccountRepositoryInterface):
    _mapper : BankAccountMapper

    def __init__(self, session : AsyncSession):
        super().__init__(session = session)
        factory = BankAccountFactory()
        self._mapper = BankAccountMapper(factory = factory)

    async def add(self, entity : BankAccount) -> None:
        orm = await self._mapper.map_to_orm(entity)
        self._session.add(orm)

    async def get(self, entity_id : UUID) -> BankAccount:
        orm = await self._session.get(BankAccountORM, entity_id)
        if not orm:
            raise KeyError()
        return await self._mapper.map_to_entity(orm)

    async def get_balance(self, user_id : UUID) -> float:
        entity = await self.get(user_id)
        if not entity:
            raise KeyError()
        return entity.balance

    async def replenish_balance(self, user_id: UUID, amount: float) -> float:
        query = update(BankAccountORM).where(BankAccountORM.user_id == user_id).values(balance = BankAccountORM.balance + amount).returning(BankAccountORM.balance)
        result = await self._session.execute(query)
        return result.scalar_one()
