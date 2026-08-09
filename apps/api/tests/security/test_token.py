
from jwt import decode

from vfdelivery.core.settings import settings
from vfdelivery.models.user import UserRole
from vfdelivery.security.token import create_access_token, get_data_from_token
from vfdelivery.shared.schemas import JWTClaims


def test_create_access_token():
    payload = JWTClaims(
        sub='test@email.com',
        role=UserRole.CUSTOMER
    )

    result = create_access_token(payload)
    access_token = result.access_token

    decoded_access_token = decode(
        access_token,
        key=settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM]
    )

    assert access_token is not None
    assert result.token_type == 'Bearer'
    assert 'exp' in decoded_access_token


def test_get_data_from_token():
    payload = JWTClaims(
        sub='test@email.com',
        role=UserRole.RESTAURANT_OWNER
    )
    access_token = create_access_token(payload).access_token

    result = get_data_from_token(access_token)
    assert result.sub == payload.sub
    assert result.role == payload.role
