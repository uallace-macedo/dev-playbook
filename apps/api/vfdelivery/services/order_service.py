from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import exists, select
from sqlalchemy.orm import Session

from vfdelivery.core.deps import SESSION
from vfdelivery.models.order import Order
from vfdelivery.models.product import Product
from vfdelivery.models.restaurant import Restaurant
from vfdelivery.schemas.order_schemas import OrderCreate


class OrderService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_order(self, order_data: OrderCreate) -> Order:
        restaurant_exists = self.session.scalar(
            select(exists().where(Restaurant.id == order_data.restaurant_id))
        )

        if not restaurant_exists:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Restaurant not found'
            )

        product = self.session.scalar(
            select(Product).where(
                Product.id == order_data.product_id,
                Product.restaurant_id == order_data.restaurant_id
            )
        )

        if not product:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="The restaurant doesn't have this product"
            )

        total_value = order_data.quantity * product.price
        order = Order(
            total_value=total_value,
            **order_data.model_dump()
        )

        self.session.add(order)
        self.session.commit()
        self.session.refresh(order)

        return order


def get_order_service(session: SESSION) -> OrderService:
    return OrderService(session)
