from ..unit_of_work_interface import UnitOfWorkInterface
from ..dto import ReplenishBalanceDTO, BankAccountBalanceDTO

class ReplenishBalanceUseCase:
    _uow : UnitOfWorkInterface

    def __init__(self, uow : UnitOfWorkInterface):
        self._uow = uow

    async def perform(self, dto : ReplenishBalanceDTO) -> BankAccountBalanceDTO:
        async with self._uow.start():
            bank_account_repository = await self._uow.get_bank_account_repository()
            balance = await bank_account_repository.replenish_balance(user_id = dto.user_id, amount = dto.amount)
            return BankAccountBalanceDTO(balance = balance)
