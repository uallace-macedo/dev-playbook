import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from vfdelivery.core.database import table_registry

if TYPE_CHECKING:
    from vfdelivery.models.restaurant import Restaurant
    from vfdelivery.models.user import User


@table_registry.mapped_as_dataclass
class Review:
    __tablename__ = 'tb_reviews'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False,
        primary_key=True,
        default_factory=uuid.uuid4
    )

    order_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('tb_orders.id'),
        unique=True
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('tb_users.id'),
        nullable=False
    )

    restaurant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('tb_restaurants.id'),
        nullable=False
    )

    rating: Mapped[int] = mapped_column(
        nullable=False
    )

    comment: Mapped[str | None] = mapped_column(
        nullable=True,
        default=None
    )

    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now()
    )

    customer: Mapped['User'] = relationship(
        init=False
    )

    restaurant: Mapped['Restaurant'] = relationship(
        init=False,
        back_populates='reviews'
    )
