from datetime import datetime
from uuid import UUID

from .entity import Entity

class OutboxMessage(Entity):

    created_at : datetime
    processed : bool
    user_id : UUID
    amount : float

    def __init__(self, order_id : UUID, user_id : UUID,
                amount: float,
                created_at : datetime = datetime.now(),
                processed : bool = False ):
        super().__init__(order_id)
        self.user_id = user_id
        self.amount = amount
        self.created_at = created_at
        self.processed = processed

    def mark_as_processed(self) -> None:
        self.processed = True

    def to_dict(self) -> dict:
        return {
            "order_id" : str(self.id),
            "user_id" : str(self.user_id),
            "amount" : self.amount
        }
