from typing import List
from uuid import UUID
from pydantic import BaseModel

from Domain.Enums.status_enum import STATUS

class OrderResponse(BaseModel):
    id : UUID
    user_id : UUID
    amount : float
    description : str
    status : STATUS

class GetOrderListResponse(BaseModel):
    orders : List[OrderResponse]

class GetOrderStatusResponse(BaseModel):
    status : STATUS

class CreateOrderRequest(BaseModel):
    amount : float
    description : str
    user_id : UUID
