from http import HTTPStatus
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import exists, select
from sqlalchemy.orm import joinedload, selectinload

from vfdelivery.core.dependencies import SessionDummy
from vfdelivery.models.order import Order, OrderStatus
from vfdelivery.models.order_item import OrderItem
from vfdelivery.models.product import Product
from vfdelivery.models.restaurant import Restaurant
from vfdelivery.schemas.order import OrderCreate, OrderFetch, OrderPatchStatus


class OrderService:
    def __init__(self, session: SessionDummy) -> None:
        self.session = session

    # n entendi
    def get_order_by_id(self, order_id: UUID) -> Order:
        stmt = (
            select(Order)
            .where(Order.id == order_id)
            .options(
                joinedload(Order.customer),
                joinedload(Order.restaurant),
                selectinload(Order.items).joinedload(OrderItem.product)
            )
        )

        order = self.session.scalar(stmt)
        if not order:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Order not found'
            )

        return order

    def _get_products_map(self, product_ids: list[UUID]) -> dict[UUID, Product]:
        """Get products from db and returns a dict {product_id: Product}."""
        stmt = select(Product).where(Product.id.in_(product_ids))
        products = self.session.scalars(stmt).all()

        if len(products) != len(product_ids):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='One or more products were not found'
            )

        return {product.id: product for product in products}

    def create(
        self,
        customer_id: UUID,
        restaurant_id: UUID,
        data: OrderCreate
    ) -> Order:
        product_ids = [item.product_id for item in data.items]
        products_map = self._get_products_map(product_ids)

        order_items = []
        total_price = 0.0

        for item in data.items:
            product = products_map[item.product_id]
            total_price += product.price * item.quantity

            order_items.append(
                OrderItem(
                    order_id=None,
                    product_id=product.id,
                    quantity=item.quantity,
                    unit_price=product.price
                )
            )

        order = Order(
            customer_id=customer_id,
            restaurant_id=restaurant_id,
            status=OrderStatus.CREATED,
            total_price=total_price,
        )

        order.items = order_items

        self.session.add(order)
        self.session.commit()

        return self.get_order_by_id(order.id)

    def get_orders_by_restaurant_id(
        self,
        owner_id: UUID,
        restaurant_id: UUID,
        options: OrderFetch
    ) -> list[Order]:
        restaurant_exists = self.session.scalar(
            select(
                exists().where(
                    Restaurant.id == restaurant_id,
                    Restaurant.owner_id == owner_id
                )
            )
        )

        if not restaurant_exists:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Restaurant not found'
            )

        stmt = (
            select(Order)
            .where(Order.restaurant_id == restaurant_id)
            .options(
                joinedload(Order.customer),
                joinedload(Order.restaurant),
                selectinload(Order.items).joinedload(OrderItem.product)
            )
        )

        if options.status:
            stmt = stmt.where(Order.status == options.status)

        stmt = (
            stmt.order_by(Order.created_at.desc())
            .limit(options.limit)
            .offset(options.offset)
        )

        orders = self.session.scalars(stmt).unique().all()
        return list(orders)

    def get_orders_by_customer_id(
        self, customer_id: UUID, options: OrderFetch
    ) -> list[Order]:
        stmt = (
            select(Order)
            .where(Order.customer_id == customer_id)
            .options(
                joinedload(Order.customer),
                joinedload(Order.restaurant),
                selectinload(Order.items).joinedload(OrderItem.product),
            )
        )

        if options.status:
            stmt = stmt.where(Order.status == options.status)

        stmt = (
            stmt.order_by(Order.created_at.desc())
            .limit(options.limit)
            .offset(options.offset)
        )

        orders = self.session.scalars(stmt).unique().all()
        return list(orders)

    def get_order_by_id_for_user(
        self, order_id: UUID, user_id: UUID
    ) -> Order:
        order = self.get_order_by_id(order_id)

        is_customer = order.customer_id == user_id
        is_owner = order.restaurant.owner_id == user_id

        if not (is_customer or is_owner):
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail='Access denied',
            )

        return order

    def update_status(
        self, owner_id: UUID, order_id: UUID, data: OrderPatchStatus
    ) -> Order:
        stmt = (
            select(Order)
            .join(Restaurant, Order.restaurant_id == Restaurant.id)
            .where(
                Order.id == order_id,
                Restaurant.owner_id == owner_id,
            )
        )

        order = self.session.scalar(stmt)

        if not order:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Order not found',
            )

        order.status = data.status

        self.session.commit()
        return self.get_order_by_id(order.id)


def get_order_service(session: SessionDummy) -> OrderService:
    return OrderService(session)
