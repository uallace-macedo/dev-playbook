import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from vfdelivery.core.database import get_session, table_registry
from vfdelivery.core.password import SecurePassword
from vfdelivery.core.token import generate_access_token
from vfdelivery.main import app
from vfdelivery.models.customer import Customer
from vfdelivery.models.product import Product
from vfdelivery.models.restaurant import Restaurant
from vfdelivery.schemas.public_schemas import AuthToken


@pytest.fixture
def client(session):
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def customer(session) -> Customer:
    customer = Customer(
        name='test',
        email='test@email.com',
        password=SecurePassword.hash(password='secret')
    )

    session.add(customer)
    session.commit()
    session.refresh(customer)

    return customer


@pytest.fixture
def restaurant(session) -> Restaurant:
    restaurant = Restaurant(
        name='test',
        email='test@email.com',
        password=SecurePassword.hash(password='secret')
    )

    session.add(restaurant)
    session.commit()
    session.refresh(restaurant)

    return restaurant


@pytest.fixture
def customer_token(customer) -> AuthToken:
    data = {'sub': customer.email}
    access_token = generate_access_token(data)

    return AuthToken(access_token=access_token)


@pytest.fixture
def restaurant_token(restaurant) -> AuthToken:
    data = {'sub': restaurant.email}
    access_token = generate_access_token(data)

    return AuthToken(access_token=access_token)


@pytest.fixture
def product(session, restaurant) -> Product:
    product = Product(
        restaurant_id=restaurant.id,
        name='X-Burguer',
        description='Test description',
        price=14.00
    )

    session.add(product)
    session.commit()
    session.refresh(product)

    return product
