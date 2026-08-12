import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from vfdelivery.core.database import table_registry
from vfdelivery.core.dependencies import get_session
from vfdelivery.main import app
from vfdelivery.models.order import Order, OrderStatus
from vfdelivery.models.order_item import OrderItem
from vfdelivery.models.product import Product
from vfdelivery.models.restaurant import Restaurant
from vfdelivery.models.review import Review
from vfdelivery.models.user import User, UserRole
from vfdelivery.schemas.auth import AuthToken, JWTClaims
from vfdelivery.security.password import create_hash
from vfdelivery.security.token import create_access_token


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
        email='customer@email.com',
        role=UserRole.CUSTOMER,
        password=create_hash('secret')
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture
def user_restaurant(session: Session) -> User:
    user = User(
        name='test',
        email='owner@email.com',
        role=UserRole.RESTAURANT_OWNER,
        password=create_hash('secret')
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture
def token_customer(user) -> AuthToken:
    payload = JWTClaims(
        sub=user.id,
        role=user.role
    )

    return create_access_token(payload)


@pytest.fixture
def token_restaurant(user_restaurant) -> AuthToken:
    payload = JWTClaims(
        sub=user_restaurant.id,
        role=user_restaurant.role
    )

    return create_access_token(payload)


@pytest.fixture
def restaurant(session: Session, user: User) -> Restaurant:
    restaurant = Restaurant(
        owner_id=user.id,
        name='Test Restaurant',
        description='Test Description'
    )

    session.add(restaurant)
    session.commit()
    session.refresh(restaurant)

    return restaurant


@pytest.fixture
def restaurant_owned(session: Session, user_restaurant: User) -> Restaurant:
    restaurant = Restaurant(
        owner_id=user_restaurant.id,
        name='Test Restaurant Owned',
        description='Test Description'
    )

    session.add(restaurant)
    session.commit()
    session.refresh(restaurant)

    return restaurant


@pytest.fixture
def product(
    session: Session,
    restaurant_owned: Restaurant,
) -> Product:
    product = Product(
        restaurant_id=restaurant_owned.id,
        name='Test Product',
        price=20.00,
    )
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


@pytest.fixture
def order(
    session: Session,
    user: User,
    restaurant_owned: Restaurant,
    product: Product,
) -> Order:
    order = Order(
        customer_id=user.id,
        restaurant_id=restaurant_owned.id,
        status=OrderStatus.CREATED,
        total_price=product.price,
    )
    order_item = OrderItem(
        order_id=None,
        product_id=product.id,
        quantity=1,
        unit_price=product.price,
    )
    order.items = [order_item]

    session.add(order)
    session.commit()
    session.refresh(order)
    return order


@pytest.fixture
def review(session: Session, user: User, order: Order) -> Review:
    order.status = OrderStatus.DELIVERED
    session.commit()

    review = Review(
        order_id=order.id,
        customer_id=user.id,
        restaurant_id=order.restaurant_id,
        rating=5,
        comment='Awesome food!'
    )

    session.add(review)
    session.commit()
    session.refresh(review)

    return review
