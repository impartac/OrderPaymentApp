from fastapi import APIRouter, Depends, Query
from uuid import UUID

from .dependencies import get_create_bank_account_use_case, get_replenish_balance_use_case, get_bank_account_balance_use_case
from .models import BankAccountBalanceResponse, BankAccountReponse, CreateBankAccountRequest, ReplenishBalanceRequest

from Application.UseCases.create_bank_account_use_case import CreateBankAccountUseCase
from Application.UseCases.replenish_balance_use_case import ReplenishBalanceUseCase
from Application.UseCases.bank_account_balance_use_case import BankAccountBalanceUseCase
from Application.dto import BankAccountIDDTO, CreateBankAccountDTO, ReplenishBalanceDTO

bank_account_router = APIRouter(prefix='/bank_account')

@bank_account_router.post(str())
async def create_order(
    create_bank_account_request : CreateBankAccountRequest,
    create_bank_account_use_case : CreateBankAccountUseCase = Depends(get_create_bank_account_use_case)
) -> BankAccountReponse:
    create_bank_account_dto = CreateBankAccountDTO(
        user_id = create_bank_account_request.user_id
    )
    bank_account_dto = await create_bank_account_use_case.perfom(create_bank_account_dto)
    return BankAccountReponse(
        user_id = bank_account_dto.user_id,
        balance = bank_account_dto.balance,
        created_at = bank_account_dto.created_at,
    )

@bank_account_router.post('/replenish')
async def replenish_balanace(
    replenish_balance_request : ReplenishBalanceRequest,
    replenish_balance_use_case : ReplenishBalanceUseCase = Depends(get_replenish_balance_use_case)
) -> BankAccountBalanceResponse:
    replenish_balance_dto = ReplenishBalanceDTO(
        user_id = replenish_balance_request.user_id,
        amount = replenish_balance_request.amount
    )
    bank_account_balance_dto  = await replenish_balance_use_case.perform(replenish_balance_dto)
    return BankAccountBalanceResponse(
        balance = bank_account_balance_dto.balance
    )

@bank_account_router.get('/balance')
async def get_balance(
    bank_account_id : UUID = Query(),
    bank_account_balance_use_case : BankAccountBalanceUseCase = Depends(get_bank_account_balance_use_case)
) -> BankAccountBalanceResponse:
    bank_account_id_dto = BankAccountIDDTO(user_id = bank_account_id) 
    bank_account_balance_dto = await bank_account_balance_use_case.perform(bank_account_id_dto)
    return BankAccountBalanceResponse(
        balance = bank_account_balance_dto.balance
    )
