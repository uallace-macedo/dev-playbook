from sqlalchemy import create_engine
from sqlalchemy.orm import registry, Session

from .settings import settings

engine = create_engine(settings.DATABASE_URL)
table_registry = registry()


def get_session():
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
