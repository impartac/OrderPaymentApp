from datetime import datetime
from uuid import UUID

from .entity import Entity

class PaymentInboxMessage(Entity):

    created_at : datetime
    user_id : UUID
    amount : float
    processed: bool

    def __init__(self, order_id : UUID, user_id : UUID,
                amount : float,
                processed: bool = False,
                created_at : datetime = datetime.now()):
        super().__init__(order_id)
        self.amount = amount
        self.user_id = user_id
        self.processed = processed
        self.created_at = created_at

    def to_dict(self) -> dict:
        return {
            "id" : str(self.id),
            "user_id" : str(self.user_id),
            "processed" : self.processed
        }
