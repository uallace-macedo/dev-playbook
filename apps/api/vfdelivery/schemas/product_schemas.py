from typing import Optional

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(min_length=2)
    description: Optional[str] = Field(default=None)
    price: float = Field(ge=0)


class ProductCreate(ProductBase):
    pass
