from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CustomerBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr


class CustomerCreate(CustomerBase):
    password: str = Field(
        min_length=6,
        description='Password must contain at least 6 characters'
    )


class CustomerUpdate(BaseModel):
    name: str | None
    email: str | None
    password: str | None


class CustomerPublic(CustomerBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)
