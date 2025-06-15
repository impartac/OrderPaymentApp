from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class ReplenishBalanceRequest(BaseModel):
    user_id : UUID
    amount : float

class CreateBankAccountRequest(BaseModel):
    user_id : UUID

class GetBankAccountBalanceRequest(BaseModel):
    user_id : UUID


class BankAccountBalanceResponse(BaseModel):
    balance : float
    
class BankAccountReponse(BaseModel):
    user_id : UUID
    balance : float
    created_at : datetime
