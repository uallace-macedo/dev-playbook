import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from vfdelivery.core.database import table_registry
from vfdelivery.core.dependencies import get_session
from vfdelivery.main import app
from vfdelivery.models.user import User, UserRole
from vfdelivery.security.password import create_hash


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
def user(session: Session) -> User:
    user = User(
        name='test',
        email='test@email.com',
        role=UserRole.CUSTOMER,
        password=create_hash('secret')
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user
