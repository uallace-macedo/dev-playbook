from http import HTTPStatus

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from vfdelivery.core.deps import SESSION
from vfdelivery.core.password import SecurePassword
from vfdelivery.core.token import generate_access_token
from vfdelivery.models.customer import Customer
from vfdelivery.schemas.customer_schemas import CustomerCreate
from vfdelivery.schemas.public_schemas import AuthToken


class CustomerService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_customer(self, data: CustomerCreate) -> Customer:
        customer = Customer(
            name=data.name,
            email=data.email,
            password=SecurePassword.hash(password=data.password)
        )

        try:
            self.session.add(customer)
            self.session.commit()
            self.session.refresh(customer)
        except IntegrityError:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already registered'
            )

        return customer

    def login_customer(self, data: OAuth2PasswordRequestForm) -> AuthToken:
        customer = self.session.scalar(
            select(Customer).where(Customer.email == data.username)
        )

        if not customer:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='Invalid email or password'
            )

        if not SecurePassword.verify(plain=data.password, hash=customer.password):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='Invalid email or password'
            )

        access_token = generate_access_token({'sub': customer.email})
        return AuthToken(access_token=access_token)


def get_customer_service(session: SESSION) -> CustomerService:
    return CustomerService(session)
