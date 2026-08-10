from http import HTTPStatus
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import exists, select

from vfdelivery.core.dependencies import SessionDummy
from vfdelivery.models.product import Product
from vfdelivery.models.restaurant import Restaurant
from vfdelivery.schemas.product import ProductCreate, ProductFetch


class ProductService:
    def __init__(self, session: SessionDummy) -> None:
        self.session = session

    def create(
        self,
        owner_id: UUID,
        restaurant_id: UUID,
        data: ProductCreate
    ) -> Product:
        restaurant = self.session.scalar(
            select(Restaurant).where(Restaurant.id == restaurant_id)
        )

        if not restaurant or not restaurant.owner_id == owner_id:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Restaurant not found'
            )

        data.name = data.name.strip()
        product_exists = self.session.scalar(
            select(exists(Product).where(
                Product.name.ilike(f'%{data.name}%'),
                Product.restaurant_id == restaurant.id
            ))
        )

        if product_exists:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Name already taken'
            )

        product = Product(
            restaurant_id=restaurant.id,
            name=data.name,
            price=data.price,
        )

        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)

        return product

    def get_products_by_restaurant_id(
        self,
        restaurant_id: UUID,
        options: ProductFetch
    ) -> list[Product]:
        stmt = select(Product).where(Product.restaurant_id == restaurant_id)

        if options.name:
            stmt = stmt.where(Product.name.ilike(f'%{options.name}%'))

        stmt = stmt.limit(options.limit).offset(options.offset)

        products = self.session.scalars(stmt).all()
        return list(products)


def get_product_service(session: SessionDummy) -> ProductService:
    return ProductService(session)
