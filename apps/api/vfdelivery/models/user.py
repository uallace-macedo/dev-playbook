import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from vfdelivery.core.database import table_registry


class UserRole(str, Enum):
    CUSTOMER = 'customer'
    RESTAURANT_OWNER = 'restaurant_owner'


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'tb_users'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False,
        primary_key=True,
        default_factory=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        nullable=False,
        unique=True
    )

    password: Mapped[str] = mapped_column(
        nullable=False
    )

    role: Mapped[UserRole] = mapped_column(
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now()
    )
