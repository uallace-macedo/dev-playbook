from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from vfdelivery.core.settings import settings
from vfdelivery.routes.auth import router as auth_router
from vfdelivery.routes.order import router as order_router
from vfdelivery.routes.product import router as product_router
from vfdelivery.routes.restaurant import router as restaurant_router
from vfdelivery.routes.review import router as review_router

app = FastAPI(title='Food Delivery API - Vecodes')

origins = [
    'http://127.0.0.1:6000',
    settings.WEB_URL
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix='/api/v1')
app.include_router(restaurant_router, prefix='/api/v1')
app.include_router(product_router, prefix='/api/v1')
app.include_router(order_router, prefix='/api/v1')
app.include_router(review_router, prefix='/api/v1')
