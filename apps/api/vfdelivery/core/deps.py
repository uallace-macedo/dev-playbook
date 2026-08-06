from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .database import get_session

SESSION = Annotated[Session, Depends(get_session)]
LOGIN_FORM_DATA = Annotated[OAuth2PasswordRequestForm, Depends()]
