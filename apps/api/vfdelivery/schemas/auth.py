
from pydantic import BaseModel, EmailStr, Field

from vfdelivery.models.user import UserRole


class AuthBase(BaseModel):
    name: str
    email: EmailStr


class AuthRegister(AuthBase):
    role: UserRole
    password: str = Field(min_length=6)


class AuthPublic(AuthBase):
    pass


class AuthToken(BaseModel):
    access_token: str
    token_type: str = 'Bearer'


class JWTClaims(BaseModel):
    sub: EmailStr
    role: UserRole
