from http import HTTPStatus
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import func, select

from vfdelivery.core.dependencies import SessionDummy
from vfdelivery.models.restaurant import Restaurant
from vfdelivery.models.review import Review
from vfdelivery.models.user import User
from vfdelivery.schemas.restaurant import (
    RestaurantCreate,
    RestaurantFetch,
)


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

    def get_restaurants(self, options: RestaurantFetch):
        stmt = (
            select(
                Restaurant.id,
                Restaurant.name,
                Restaurant.description,

                func.coalesce(func.avg(Review.rating), 0.0).label('rating_average'),
                func.count(Review.id).label('total_reviews')
            )
            .outerjoin(Review, Restaurant.id == Review.restaurant_id)
            .group_by(Restaurant.id)
            .limit(options.limit)
            .offset(options.offset)
        )

        if options.name:
            stmt = stmt.where(Restaurant.name.ilike(f'%{options.name}%'))

        return self.session.execute(stmt).mappings().all()

    def get_restaurant_by_id(self, restaurant_id: UUID):
        stmt = (
            select(
                Restaurant.id,
                Restaurant.name,
                Restaurant.description,

                func.coalesce(func.avg(Review.rating), 0.0).label('rating_average'),
                func.count(Review.id).label('total_reviews'),
            )
            .outerjoin(Review, Restaurant.id == Review.restaurant_id)
            .group_by(Restaurant.id)
            .where(Restaurant.id == restaurant_id)
        )

        result = self.session.execute(stmt).mappings().first()
        if not result:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Restaurant not found'
            )

        return result


def get_restaurant_service(session: SessionDummy) -> RestaurantService:
    return RestaurantService(session)
