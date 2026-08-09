from fastapi import FastAPI

from vfdelivery.routes.auth import router as auth_router
from vfdelivery.routes.restaurant import router as restaurant_router

app = FastAPI(title='Food Delivery API - Vecodes', root_path='/api/v1')
app.include_router(auth_router)
app.include_router(restaurant_router)
