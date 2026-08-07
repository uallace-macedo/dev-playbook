from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RestaurantBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr


class RestaurantCreate(RestaurantBase):
    password: str = Field(
        min_length=6,
        description='Password must contain at least 6 digits'
    )


class RestaurantPublic(RestaurantBase):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )


class RestaurantList(BaseModel):
    restaurants: list[RestaurantPublic]
