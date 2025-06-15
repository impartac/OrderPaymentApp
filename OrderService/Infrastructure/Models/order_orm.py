from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Float, String
from sqlalchemy.dialects.postgresql import ENUM as SQLEnum
from sqlalchemy import UUID as SQLUUID
from sqlalchemy.dialects.postgresql import UUID as UUIDps

from .base_orm import BaseORM

from Domain.Enums.status_enum import STATUS

class OrderORM(BaseORM):
    __tablename__ = "orders"
    __table_args__ = {"schema": "order_storage"}

    
    id: Mapped[UUID] = mapped_column(
        UUIDps(as_uuid=True),
        primary_key=True,
    )
    user_id: Mapped[UUID] = mapped_column(SQLUUID, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String(2000))
    status: Mapped[STATUS] = mapped_column(
        SQLEnum(STATUS, name="status", schema="order_storage"),
        nullable=False
    )
