from uuid import UUID
from datetime import datetime

from Domain.Enums.status_enum import STATUS
from Domain.Entities.entity import Entity

class Order(Entity):
    user_id : UUID
    amount : float
    description : str
    status : STATUS
    created_at : datetime

    def __init__(self, entity_id : UUID, user_id : UUID, 
                amount : float, description : str, 
                status : STATUS, created_at : datetime = datetime.now()):
        super().__init__(entity_id)
        self.user_id = user_id
        self.amount = amount
        self.description = description
        self.status = status
        self.created_at = created_at
