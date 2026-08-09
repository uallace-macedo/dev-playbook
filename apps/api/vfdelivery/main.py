from contextlib import asynccontextmanager

from fastapi import FastAPI

from vfdelivery.core.database import create_db_and_tables
from vfdelivery.routes.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title='Food Delivery API - Vecodes',
    root_path='/api/v1',
    lifespan=lifespan
)
app.include_router(auth_router)
