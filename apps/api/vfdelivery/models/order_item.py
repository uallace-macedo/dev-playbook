import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from vfdelivery.core.database import table_registry
from vfdelivery.models.product import Product


@table_registry.mapped_as_dataclass
class OrderItem:
    __tablename__ = 'tb_order_items'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False,
        primary_key=True,
        default_factory=uuid.uuid4
    )

    order_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('tb_orders.id'),
        nullable=False
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('tb_products.id'),
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

    product: Mapped['Product'] = relationship(
        init=False
    )

    @property
    def subtotal(self) -> float:
        return self.quantity * self.unit_price

    @property
    def product_name(self) -> str:
        return self.product.name if self.product else ''
