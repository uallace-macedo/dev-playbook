import uuid
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from vfdelivery.core.database import table_registry


@table_registry.mapped_as_dataclass
class Restaurant:
    __tablename__ = 'tb_restaurants'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False,
        primary_key=True,
        default_factory=uuid.uuid4
    )

    owner_id: Mapped[uuid.UUID] = mapped_column(
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
