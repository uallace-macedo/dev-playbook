from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(min_length=2)
    description: Optional[str] = Field(default=None)
    price: float = Field(ge=0)


class ProductCreate(ProductBase):
    pass


class ProductPublic(ProductBase):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )


class ProductList(BaseModel):
    products: list[ProductPublic]
