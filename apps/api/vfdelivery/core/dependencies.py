from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from vfdelivery.core.database import get_session
from vfdelivery.models.user import UserRole
from vfdelivery.schemas.auth import JWTClaims
from vfdelivery.security.token import get_current_user

SessionDummy = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[JWTClaims, Depends(get_current_user)]
LoginFormData = Annotated[OAuth2PasswordRequestForm, Depends()]


class RoleChecker:
    def __init__(self, allowed_routes: list[UserRole]) -> None:
        self.allowed_routes = allowed_routes

    def __call__(self, current_user: CurrentUser) -> JWTClaims:
        if current_user.role not in self.allowed_routes:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail='Access denied'
            )

        return current_user


RequireRestaurantOwner = Annotated[JWTClaims, Depends(RoleChecker([UserRole.RESTAURANT_OWNER]))]
