import uuid
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from vfdelivery.core.database import table_registry


@table_registry.mapped_as_dataclass
class Review:
    __tablename__ = 'tb_reviews'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False,
        primary_key=True,
        default_factory=uuid.uuid4
    )

    order_id: Mapped[uuid.UUID] = mapped_column(
        nullable=False,
        unique=True
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(
        nullable=False
    )

    rating: Mapped[int] = mapped_column(
        nullable=False
    )

    comment: Mapped[float] = mapped_column(
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now()
    )
