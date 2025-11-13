from fastapi import HTTPException, Body, APIRouter, Depends
from .auth import get_current_user
from starlette import status
from ..models import Users
from ..dependencies import db_dependency, bcrypt_context
from typing import Annotated



router = APIRouter(
    prefix="/user",
    tags=["user"]
)


user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def read_current_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return db.query(Users).filter(Users.id == user.get("id")).first()


@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, new_password: str = Body(min_length=6)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")

    new_hashed_password = bcrypt_context.hash(new_password)
    user_model.hashed_password = new_hashed_password

    db.add(user_model)
    db.commit()


@router.put("/change_phone_number", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, db: db_dependency, new_phone_number: str = Body(min_length=10, max_length=15)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_model.phone_number = new_phone_number

    db.add(user_model)
    db.commit()