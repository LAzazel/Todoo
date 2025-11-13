from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from .database import SessionLocal
from passlib.context import CryptContext


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency: type[Session] = Annotated[Session, Depends(get_db)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
