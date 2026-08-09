import uuid
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from vfdelivery.core.database import table_registry


@table_registry.mapped_as_dataclass
class OrderItem:
    __tablename__ = 'tb_order_items'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False,
        primary_key=True,
        default_factory=uuid.uuid4
    )

    order_id: Mapped[uuid.UUID] = mapped_column(
        nullable=False
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        nullable=False
    )

    unit_price: Mapped[float] = mapped_column(
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now()
    )
