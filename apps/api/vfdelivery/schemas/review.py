from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ReviewBase(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = Field(default=None)


class ReviewCreate(ReviewBase):
    order_id: UUID


class ReviewPublic(ReviewCreate):
    id: UUID
    customer_id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )


class ReviewFetch(BaseModel):
    limit: int = Field(ge=0, default=10)
    offset: int = Field(ge=0, default=0)
