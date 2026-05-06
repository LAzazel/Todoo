from datetime import timedelta, datetime, timezone
from enum import Enum
from sqlalchemy.exc import IntegrityError
from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from .models import Users
from pydantic import BaseModel, EmailStr
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from .dependencies import db_dependency, bcrypt_context
from .config import SECRET_KEY, ALGORITHM, SECRET_KEY_PREVIOUS

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

class UserRole(str, Enum):
    user = "user"
    admin = "admin"


class CreateUserRequest(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    phone_number: str
    role: UserRole = UserRole.user


class Token(BaseModel):
    access_token: str
    token_type: str


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(user_name: str, user_id: int, role:str, expires_delta:timedelta):
    encode: dict[str, Any] = {"sub": user_name, "id": user_id, "role": role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': int(expires.timestamp())})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    keys_to_try = [SECRET_KEY]
    if SECRET_KEY_PREVIOUS:
        keys_to_try.append(SECRET_KEY_PREVIOUS)

    for key in keys_to_try:
        try:
            payload = jwt.decode(token, key, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            user_id: int = payload.get("id")
            user_role: str = payload.get("role")
            if username is None or user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
            return {"username": username, "id": user_id, "role": user_role}
        except JWTError:
            continue

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=str(create_user_request.email),
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        role=create_user_request.role,
        phone_number=create_user_request.phone_number,
        is_active=True
    )
    try:
        db.add(create_user_model)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Username or email already exists")
    


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    token = create_access_token(user.username, user.id, user.role, expires_delta=timedelta(minutes=20))

    return {"access_token": token, "token_type": "bearer"}
