from uuid import UUID
from datetime import datetime

from Domain.Entities.entity import Entity

class BankAccount(Entity):
    balance : float
    created_at : datetime

    def __init__(self, user_id : UUID, balance : float = 0, created_at : datetime = datetime.now()):
        super().__init__(user_id)
        self.balance = balance
        self.created_at = created_at
