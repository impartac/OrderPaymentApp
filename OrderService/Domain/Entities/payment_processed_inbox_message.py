from uuid import UUID

from .entity import Entity

class PaymentProcessedInboxMessage(Entity):
    
    is_success : bool
    description : str
    processed : bool
    
    def __init__(self, order_id : UUID, is_success: bool, description : str, processed: bool):
        super().__init__(order_id)
        self.is_success = is_success
        self.description = description
        self.processed = processed
        
    def to_dict(self):
        return {
            "order_id" : str(self.id),
            "is_success" : self.is_success,
            "description" : self.description
        }