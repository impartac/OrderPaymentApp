from ..dto import BankAccountBalanceDTO, BankAccountIDDTO
from ..unit_of_work_interface import UnitOfWorkInterface


class BankAccountBalanceUseCase:
    _uow : UnitOfWorkInterface

    def __init__(self, uow : UnitOfWorkInterface):
        self._uow = uow

    async def perform(self, dto : BankAccountIDDTO) -> BankAccountBalanceDTO:
        async with self._uow.start():
            bank_account_repository = await self._uow.get_bank_account_repository()
            balance = await bank_account_repository.get_balance(user_id = dto.user_id)
            return BankAccountBalanceDTO(balance = balance)
