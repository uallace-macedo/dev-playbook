from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import HTTPException
from jwt import PyJWTError, decode, encode

from vfdelivery.core.settings import settings
from vfdelivery.models.user import UserRole
from vfdelivery.shared.schemas import AuthToken, JWTClaims


def create_access_token(data: JWTClaims) -> AuthToken:
    payload = data.model_dump()

    exp = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.TOKEN_EXPIRES_MINUTES
    )

    payload.update({'exp': exp})
    token = encode(
        payload,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return AuthToken(
        access_token=token,
        token_type='Bearer'
    )


def get_data_from_token(token: str) -> JWTClaims:
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate token'
    )

    try:
        payload = decode(
            token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        email: str | None = payload.get('sub')
        role: UserRole | None = payload.get('role')

        if not email or not role:
            raise credentials_exception

        return JWTClaims(
            sub=email,
            role=role
        )

    except PyJWTError:
        raise credentials_exception
