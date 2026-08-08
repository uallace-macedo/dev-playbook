import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from vfdelivery.core.database import table_registry


class OrderStatus(str, Enum):
    CREATED = 'created'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    DELIVERED = 'delivered'
    REVIEWED = 'reviewed'


@table_registry.mapped_as_dataclass
class Order:
    __tablename__ = 'tb_orders'

    id: Mapped[uuid.UUID] = mapped_column(
            init=False,
            primary_key=True,
            default_factory=uuid.uuid4
        )

    customer_id: Mapped[uuid.UUID] = mapped_column(
        nullable=False
    )

    restaurant_id: Mapped[uuid.UUID] = mapped_column(
        nullable=False
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        nullable=False
    )

    total_value: Mapped[float] = mapped_column(
            nullable=False
        )

    quantity: Mapped[int] = mapped_column(
        default=1
    )

    status: Mapped[str] = mapped_column(
        default=OrderStatus.CREATED
    )

    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now()
    )
