from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import FLOAT, UUID as SQLUUID
from sqlalchemy import ForeignKey, DateTime, Boolean

from .base_orm import BaseORM

class OrderCreatedOutboxMessageORM(BaseORM):
    __tablename__ = "order_created_messages"
    __table_args__ = {"schema": "order_storage"}

    order_id: Mapped[UUID] = mapped_column(SQLUUID,
                                    ForeignKey("order_storage.orders.id"),
                                    nullable=False,
                                    primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )
    processed : Mapped[bool] = mapped_column(
        Boolean,
        nullable = False,
        default = False
    )
    
    user_id: Mapped[UUID] = mapped_column(SQLUUID, nullable = False)
    amount : Mapped[float] = mapped_column(FLOAT, nullable = False)
