from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID as SQLUUID
from sqlalchemy import Boolean, String

from .base_orm import BaseORM

class PaymentProcessedInboxMessageORM(BaseORM):
    __tablename__ = "payment_processed_inbox_messages"
    __table_args__ = {"schema": "order_storage"}

    order_id: Mapped[UUID] = mapped_column(SQLUUID,
                                    nullable=False,
                                    primary_key=True)

    is_success : Mapped[bool] = mapped_column(
        Boolean,
        nullable = False,
        default = False
    )

    description: Mapped[str] = mapped_column(String, nullable = False)

    processed: Mapped[bool] = mapped_column(Boolean, nullable = False)
