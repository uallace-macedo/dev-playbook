from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .database import get_session


@dataclass
class PaginationParams:
    limit: int = Query(default=10)
    offset: int = Query(default=0)


SESSION = Annotated[Session, Depends(get_session)]
LOGIN_FORM_DATA = Annotated[OAuth2PasswordRequestForm, Depends()]
PAGINATION = Annotated[PaginationParams, Depends()]
