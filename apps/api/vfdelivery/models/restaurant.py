import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from vfdelivery.core.database import table_registry

if TYPE_CHECKING:
    from vfdelivery.models.review import Review
    from vfdelivery.models.user import User


@table_registry.mapped_as_dataclass
class Restaurant:
    __tablename__ = 'tb_restaurants'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False,
        primary_key=True,
        default_factory=uuid.uuid4
    )

    owner_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('tb_users.id'),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now()
    )

    customer: Mapped['User'] = relationship(
        init=False
    )

    reviews: Mapped[List['Review']] = relationship(
        init=False,
        back_populates='restaurant'
    )
