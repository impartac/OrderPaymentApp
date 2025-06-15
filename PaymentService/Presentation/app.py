from fastapi import FastAPI

from .router import bank_account_router

app = FastAPI(title="Payment Service")

app.include_router(bank_account_router, prefix='/api/v1')