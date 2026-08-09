from uuid import UUID

from pydantic import BaseModel, ConfigDict

from vfdelivery.models.user import UserRole


class UserBase(BaseModel):
    name: str
    email: str
    role: UserRole


class UserPublic(UserBase):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )
