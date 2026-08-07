from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError, decode, encode
from sqlalchemy import select

from vfdelivery.core.deps import SESSION
from vfdelivery.models.customer import Customer
from vfdelivery.models.restaurant import Restaurant

from .settings import settings

SECRET_KEY: str = settings.JWT_SECRET
ALGORITHM: str = 'HS256'
TOKEN_EXP_MINUTES: int = 30

OAUTH2_SCHEMA_CUSTOMER = OAuth2PasswordBearer(tokenUrl='/customer/login')
OAUTH2_SCHEMA_RESTAURANT = OAuth2PasswordBearer(tokenUrl='/restaurant/login')

OSCustomer = Annotated[OAuth2PasswordBearer, Depends(OAUTH2_SCHEMA_CUSTOMER)]
OSRestaurant = Annotated[OAuth2PasswordBearer, Depends(OAUTH2_SCHEMA_RESTAURANT)]


def generate_access_token(data: dict) -> str:
    claims = data.copy()

    exp = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=TOKEN_EXP_MINUTES
    )

    claims.update({'exp': exp})
    return encode(claims, key=SECRET_KEY, algorithm=ALGORITHM)


def get_email_from_token(token: str) -> str:
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get('sub')

        if not email:
            raise credentials_exception

        return email

    except PyJWTError:
        raise credentials_exception


def get_current_customer(
    session: SESSION,
    token: OSCustomer
) -> Customer:
    email = get_email_from_token(token)
    customer = session.scalar(select(Customer).where(Customer.email == email))

    if not customer:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return customer


def get_current_restaurant(
    session: SESSION,
    token: OSRestaurant
) -> Restaurant:
    email = get_email_from_token(token)
    restaurant = session.scalar(select(Restaurant).where(Restaurant.email == email))

    if not restaurant:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return restaurant
