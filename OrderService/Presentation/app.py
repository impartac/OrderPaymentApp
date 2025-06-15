from fastapi import FastAPI

from .router import order_router

app = FastAPI(title="Order Service")

app.include_router(order_router, prefix='/api/v1')