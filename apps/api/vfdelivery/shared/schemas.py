from pydantic import BaseModel, EmailStr

from vfdelivery.models.user import UserRole


class JWTClaims(BaseModel):
    sub: EmailStr
    role: UserRole


class AuthToken(BaseModel):
    access_token: str
    token_type: str = 'Bearer'
