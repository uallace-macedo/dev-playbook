from http import HTTPStatus
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import exists, select

from vfdelivery.core.dependencies import SessionDummy
from vfdelivery.models.order import Order, OrderStatus
from vfdelivery.models.restaurant import Restaurant
from vfdelivery.models.review import Review
from vfdelivery.schemas.review import ReviewCreate, ReviewFetch


class ReviewService:
    def __init__(self, session: SessionDummy) -> None:
        self.session = session

    def create(
        self, customer_id: UUID, order_id: UUID, data: ReviewCreate
    ) -> Review:
        order = self.session.scalar(
            select(Order).where(
                Order.id == order_id,
                Order.customer_id == customer_id,
            )
        )

        if not order:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Order not found',
            )

        review_exists = self.session.scalar(
            select(
                exists().where(
                    Review.order_id == order_id,
                    Review.customer_id == customer_id,
                )
            )
        )

        if review_exists:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail='Order already reviewed',
            )

        if order.status != OrderStatus.DELIVERED:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail='Order is not delivered yet',
            )

        review = Review(
            order_id=order_id,
            customer_id=customer_id,
            restaurant_id=order.restaurant_id,
            rating=data.rating,
            comment=data.comment,
        )

        order.reviewed = True
        self.session.add(review)
        self.session.commit()
        self.session.refresh(review)

        return review

    def get_reviews_by_restaurant_id(
        self, restaurant_id: UUID, options: ReviewFetch
    ) -> list[Review]:
        restaurant_exists = self.session.scalar(
            select(
                exists().where(
                    Restaurant.id == restaurant_id
                )
            )
        )

        if not restaurant_exists:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Restaurant not found',
            )

        reviews = self.session.scalars(
            select(Review)
            .where(Review.restaurant_id == restaurant_id)
            .limit(options.limit)
            .offset(options.offset)
        )

        return list(reviews)


def get_review_service(session: SessionDummy) -> ReviewService:
    return ReviewService(session)
