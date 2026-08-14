from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Annotated, Optional
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError, decode, encode
from pydantic import ValidationError

from vfdelivery.core.settings import settings
from vfdelivery.schemas.auth import AuthToken, JWTClaims

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')
oauth2_scheme_optional = OAuth2PasswordBearer(
    tokenUrl='/api/v1/auth/login',
    auto_error=False
)
Token = Annotated[str, Depends(oauth2_scheme)]
OptionalToken = Annotated[Optional[str], Depends(oauth2_scheme_optional)]


def create_access_token(data: JWTClaims) -> AuthToken:
    payload = data.model_dump(mode='json')

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


def get_current_user(token: Token) -> JWTClaims:
    """Get authenticated user's data (`email` and `role`) from Bearer token"""
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

        return JWTClaims(**payload)

    except (ValidationError, PyJWTError):
        raise credentials_exception


def get_optional_current_user(token: OptionalToken) -> Optional[JWTClaims]:
    """Retrieves authenticated user's data if token is provided, otherwise None"""
    if not token:
        return None

    try:
        payload = decode(
            token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return JWTClaims(**payload)

    except (ValidationError, PyJWTError):
        return None
