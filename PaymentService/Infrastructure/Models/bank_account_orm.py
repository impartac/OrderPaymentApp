from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Float, DateTime
from sqlalchemy.dialects.postgresql import UUID as UUIDps

from .base_orm import BaseORM

class BankAccountORM(BaseORM):
    __tablename__ = "bank_accounts"
    __table_args__ = {"schema": "payment_storage"}

    user_id: Mapped[UUID] = mapped_column(
        UUIDps(as_uuid=True),
        primary_key=True,
    )
    balance: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable = False)
