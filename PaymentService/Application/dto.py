from uuid import UUID
from datetime import datetime

class CreateBankAccountDTO:
    user_id : UUID

    def __init__(self, user_id : UUID):
        self.user_id = user_id

class ReplenishBalanceDTO:
    user_id : UUID
    amount : float
    
    def __init__(self, user_id : UUID, amount : float):
        self.user_id = user_id
        self.amount = amount

class BankAccountIDDTO:
    user_id : UUID
    
    def __init__(self, user_id : UUID):
        self.user_id = user_id

class BankAccountBalanceDTO:
    balance : float
    
    def __init__(self, balance : float):
        self.balance = balance
        
        
class BankAccountDTO:
    user_id : UUID
    balance : float
    created_at : datetime
    
    def __init__(self, user_id : UUID, balance : float, created_at : datetime):
        self.user_id = user_id
        self.balance = balance
        self.created_at = created_at

