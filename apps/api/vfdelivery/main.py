from fastapi import FastAPI

from vfdelivery.routes.auth import router as auth_router
from vfdelivery.routes.order import router as order_router
from vfdelivery.routes.product import router as product_router
from vfdelivery.routes.restaurant import router as restaurant_router
from vfdelivery.routes.review import router as review_router

app = FastAPI(title='Food Delivery API - Vecodes')
app.include_router(auth_router, prefix='/api/v1')
app.include_router(restaurant_router, prefix='/api/v1')
app.include_router(product_router, prefix='/api/v1')
app.include_router(order_router, prefix='/api/v1')
app.include_router(review_router, prefix='/api/v1')
