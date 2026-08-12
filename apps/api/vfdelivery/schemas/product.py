from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(min_length=2)
    price: float = Field(ge=0)


class ProductCreate(ProductBase):
    pass


class ProductFetch(BaseModel):
    limit: int = Field(ge=0, default=10)
    offset: int = Field(ge=0, default=0)
    name: Optional[str] = Field(default=None)


class ProductPublic(ProductCreate):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )


class ProductList(BaseModel):
    products: list[ProductPublic]
