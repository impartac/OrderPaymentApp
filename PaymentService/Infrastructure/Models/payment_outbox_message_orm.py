from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import  UUID as SQLUUID, String
from sqlalchemy import ForeignKey, Boolean

from .base_orm import BaseORM

class PaymentOutboxMessageORM(BaseORM):
    __tablename__ = "outbox_messages"
    __table_args__ = {"schema": "payment_storage"}

    order_id: Mapped[UUID] = mapped_column(SQLUUID,
                                    ForeignKey('payment_storage.inbox_messages.order_id'),
                                    nullable=False,
                                    primary_key=True)

    is_success : Mapped[bool] = mapped_column(
        Boolean,
        nullable = False,
        default = False
    )

    description: Mapped[str] = mapped_column(String, nullable = False)

    processed: Mapped[bool] = mapped_column(Boolean, nullable = False)
