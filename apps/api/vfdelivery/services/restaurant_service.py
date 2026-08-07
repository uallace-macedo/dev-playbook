from http import HTTPStatus

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from vfdelivery.core.deps import SESSION
from vfdelivery.core.password import SecurePassword
from vfdelivery.core.token import generate_access_token
from vfdelivery.models.restaurant import Restaurant
from vfdelivery.schemas.public_schemas import AuthToken
from vfdelivery.schemas.restaurant_schemas import RestaurantCreate


class RestaurantService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_restaurant(self, data: RestaurantCreate) -> Restaurant:
        try:
            restaurant = Restaurant(
                name=data.name,
                email=data.email,
                password=SecurePassword.hash(password=data.password)
            )

            self.session.add(restaurant)
            self.session.commit()
            self.session.refresh(restaurant)
        except IntegrityError:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already taken'
            )

        return restaurant

    def login_restaurant(self, data: OAuth2PasswordRequestForm) -> AuthToken:
        restaurant = self.session.scalar(
            select(Restaurant).where(Restaurant.email == data.username)
        )

        if not restaurant:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='Invalid email or password'
            )

        if not SecurePassword.verify(plain=data.password, hash=restaurant.password):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='Invalid email or password'
            )

        access_token = generate_access_token({'sub': restaurant.email})
        return AuthToken(access_token=access_token)


def get_restaurant_service(session: SESSION) -> RestaurantService:
    return RestaurantService(session)
