from sqlalchemy import create_engine
from sqlalchemy.orm import Session, registry

from vfdelivery.core.settings import settings

table_registry = registry()
engine = create_engine(settings.sync_database_url)


def get_session():
    with Session(engine) as session:
        yield session
