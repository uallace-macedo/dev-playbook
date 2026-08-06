import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from vfdelivery.core.database import get_session, table_registry
from vfdelivery.main import app

from vfdelivery.schemas.customer_schemas import CustomerCreate
from vfdelivery.models.customer import Customer
from vfdelivery.core.password import SecurePassword
from sqlalchemy.pool import StaticPool


@pytest.fixture
def client(session):
    def get_session_override():
        yield session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
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
