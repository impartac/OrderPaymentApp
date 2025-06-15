from fastapi import APIRouter, Depends, Query
from uuid import UUID

from .dependencies import get_create_order_use_case, get_order_list_use_case, get_order_status_use_case
from .models import CreateOrderRequest, GetOrderListResponse, GetOrderStatusResponse, OrderResponse

from Application.UseCases.create_order_use_case import CreateOrderUseCase
from Application.UseCases.order_list_use_case import OrderListUseCase
from Application.UseCases.order_status_use_case import OrderStatusUseCase
from Application.dto import CreateOrderDTO

order_router = APIRouter(prefix='/order')

@order_router.post(str())
async def create_order(
    create_order_request : CreateOrderRequest,
    create_order_use_case : CreateOrderUseCase = Depends(get_create_order_use_case)
) -> OrderResponse:
    create_order_dto = CreateOrderDTO(
        amount = create_order_request.amount,
        user_id = create_order_request.user_id,
        description = create_order_request.description
    )
    order = await create_order_use_case.perfom(create_order_dto)
    return OrderResponse(
        id = order.id,
        user_id = order.id,
        amount = order.amount,
        description = order.description,
        status = order.status
    )

@order_router.get(str())
async def get_order(
    user_id : UUID = Query(),
    order_list_use_case : OrderListUseCase = Depends(get_order_list_use_case)
) -> GetOrderListResponse:
    order_list = await order_list_use_case.perform(user_id = user_id)
    return GetOrderListResponse(
        orders = [OrderResponse(id = order.id,
                                user_id = order.id,
                                amount = order.amount,
                                description = order.description,
                                status = order.status)
                  for order in order_list]
    )

@order_router.get('/status')
async def get_status(
    order_id : UUID = Query(),
    order_status_use_case : OrderStatusUseCase = Depends(get_order_status_use_case)
) -> GetOrderStatusResponse:
    status = await order_status_use_case.perform(order_id = order_id)
    return GetOrderStatusResponse(status = status)
