from sqlalchemy import create_engine
from sqlalchemy.orm import Session, registry

from vfdelivery.core.settings import settings

table_registry = registry()
engine = create_engine(settings.DATABASE_URL)


def create_db_and_tables():
    table_registry.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
