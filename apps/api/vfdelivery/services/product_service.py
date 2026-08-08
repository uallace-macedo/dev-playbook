from http import HTTPStatus
from typing import Sequence
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import exists, select
from sqlalchemy.orm import Session

from vfdelivery.core.deps import SESSION
from vfdelivery.models.product import Product
from vfdelivery.models.restaurant import Restaurant
from vfdelivery.schemas.product_schemas import ProductCreate


class ProductService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_product(
        self,
        *,
        restaurant_id: UUID,
        product_data: ProductCreate
    ) -> Product:
        restaurant_exists = self.session.scalar(
            select(exists().where(Restaurant.id == restaurant_id))
        )

        if not restaurant_exists:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Restaurant not found'
            )

        product_data.name = product_data.name.strip()
        product_exists = self.session.scalar(
            select(exists().where(
                Product.name.ilike(product_data.name),
                Product.restaurant_id == restaurant_id
            ))
        )

        if product_exists:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='A product with this name already exists'
            )

        product = Product(
            restaurant_id=restaurant_id,
            **product_data.model_dump()
        )

        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)

        return product

    def get_products_by_restaurant(
        self,
        restaurant_id: UUID,
        *,
        limit: int = 10,
        offset: int = 0,
        name: str = None
    ) -> Sequence[Product]:
        restaurant_exists = self.session.scalar(
            select(exists().where(Restaurant.id == restaurant_id))
        )

        if not restaurant_exists:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Restaurant not found'
            )

        stmt = select(Product).where(
            Product.restaurant_id == restaurant_id
        )

        if name:
            stmt = stmt.where(
                Product.name.ilike(f'%{name}%'),
            )

        stmt = stmt.limit(limit).offset(offset)
        return self.session.scalars(stmt).all()


def get_product_service(session: SESSION) -> ProductService:
    return ProductService(session)
