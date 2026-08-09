from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class RestaurantBase(BaseModel):
    name: str
    description: Optional[str] = Field(default=None)


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantPublic(RestaurantBase):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )


class RestaurantFetch(BaseModel):
    limit: int = Field(gt=0, default=10)
    offset: int = Field(ge=0, default=0)
    name: Optional[str] = Field(default=None)


class RestaurantList(BaseModel):
    restaurants: list[RestaurantPublic]
