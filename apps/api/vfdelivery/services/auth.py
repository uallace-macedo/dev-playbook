from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from vfdelivery.core.dependencies import LoginFormData, SessionDummy
from vfdelivery.models.user import User
from vfdelivery.schemas.auth import AuthRegister, AuthToken, JWTClaims
from vfdelivery.security.password import create_hash, verify
from vfdelivery.security.token import create_access_token


class AuthService:
    def __init__(self, session: SessionDummy) -> None:
        self.session = session

    def register(self, data: AuthRegister) -> User:
        try:
            user = User(
                name=data.name,
                email=data.email,
                role=data.role,
                password=create_hash(data.password),
            )

            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)

            return user

        except IntegrityError:
            self.session.rollback()
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already taken'
            )

        except Exception as e:
            print(str(e))
            self.session.rollback()
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail='Internal server error'
            )

    def login(self, data: LoginFormData) -> AuthToken:
        invalid_credentials = HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Invalid credentials'
        )

        email = data.username

        user = self.session.scalar(
            select(User).where(User.email == email)
        )

        if not user:
            raise invalid_credentials

        password = data.password
        if not verify(password, user.password):
            raise invalid_credentials

        payload = JWTClaims(sub=user.email, role=user.role)
        access_token = create_access_token(payload).access_token

        return AuthToken(access_token=access_token)


def get_auth_service(session: SessionDummy) -> AuthService:
    return AuthService(session)
