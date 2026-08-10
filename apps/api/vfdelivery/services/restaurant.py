from http import HTTPStatus
from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select

from vfdelivery.core.dependencies import SessionDummy
from vfdelivery.models.restaurant import Restaurant
from vfdelivery.models.user import User
from vfdelivery.schemas.restaurant import RestaurantCreate, RestaurantFetch


class RestaurantService:
    def __init__(self, session: SessionDummy) -> None:
        self.session = session

    def create(self, owner_id: str, data: RestaurantCreate) -> Restaurant:
        user = self.session.scalar(
            select(User).where(User.id == owner_id)
        )

        if not user:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='User not found'
            )

        restaurant = Restaurant(
            owner_id=user.id,
            name=data.name,
            description=data.description,
        )

        self.session.add(restaurant)
        self.session.commit()
        self.session.refresh(restaurant)

        return restaurant

    def get_restaurants(self, fetch_data: RestaurantFetch) -> Sequence[Restaurant]:
        stmt = select(Restaurant)

        if fetch_data.name:
            stmt = stmt.where(Restaurant.name.ilike(f'%{fetch_data.name}%'))

        stmt = stmt.limit(
            fetch_data.limit
        ).offset(
            fetch_data.offset
        ).order_by(
            Restaurant.name.asc()
        )

        return self.session.scalars(stmt).all()


def get_restaurant_service(session: SessionDummy) -> RestaurantService:
    return RestaurantService(session)
