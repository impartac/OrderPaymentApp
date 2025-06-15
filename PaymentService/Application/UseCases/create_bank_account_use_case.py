from ..unit_of_work_interface import UnitOfWorkInterface
from ..dto import BankAccountDTO, CreateBankAccountDTO
from ..mappers import DTOBankAccountMapper


class CreateBankAccountUseCase:
    _uow : UnitOfWorkInterface
    _dto_bank_account_mapper : DTOBankAccountMapper

    def __init__(self, uow : UnitOfWorkInterface,
                dto_bank_account_mapper : DTOBankAccountMapper):
        self._uow = uow
        self._dto_bank_account_mapper = dto_bank_account_mapper

    async def perfom(self, order_create_dto : CreateBankAccountDTO) -> BankAccountDTO:
        bank_account = await self._dto_bank_account_mapper.map_from_dto(order_create_dto)
        async with self._uow.start():
            bank_account_repository = await self._uow.get_bank_account_repository()
            await bank_account_repository.add(bank_account)
            return BankAccountDTO(
                user_id = bank_account.id,
                balance = bank_account.balance,
                created_at = bank_account.created_at
            )
