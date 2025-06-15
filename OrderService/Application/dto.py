from uuid import UUID


class CreateOrderDTO:
    amount : float
    user_id : UUID
    description : str
    
    def __init__(self, amount : float, user_id : UUID, description : str):
        self.amount = amount
        self.user_id = user_id
        self.description = description
    
