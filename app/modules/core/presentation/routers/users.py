from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field


from app.modules.core.application.queries.users.get_profile import GetProfileQuery, GetProfileHandler
from app.modules.core.application.commands.users.change_password import ChangePasswordCommand, ChangePasswordHandler
from app.modules.core.application.commands.users.change_phone import ChangePhoneCommand, ChangePhoneHandler

from app.modules.core.presentation.dependencies import (
    get_current_user_id,
    get_profile_handler,
    get_change_password_handler,
    get_change_phone_handler
)

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


class ChangePasswordRequest(BaseModel):
    new_password: str = Field(min_length=6)

class ChangePhoneNumberRequest(BaseModel):
    new_phone_number: str = Field(min_length=10, max_length=15)

class UserProfileResponse(BaseModel):
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    phone_number: str
    role: str


@router.get("/", response_model=UserProfileResponse, status_code=status.HTTP_200_OK)
def read_current_user(
    user_id: int = Depends(get_current_user_id),
    handler: GetProfileHandler = Depends(get_profile_handler)
):
    query = GetProfileQuery(user_id=user_id)
    return handler.execute(query)

@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(
    request: ChangePasswordRequest,
    user_id: int = Depends(get_current_user_id),
    handler: ChangePasswordHandler = Depends(get_change_password_handler)
):
    command = ChangePasswordCommand(user_id=user_id, new_password=request.new_password)
    handler.execute(command)

@router.put("/change_phone_number", status_code=status.HTTP_204_NO_CONTENT)
def change_phone_number(
    request: ChangePhoneNumberRequest,
    user_id: int = Depends(get_current_user_id),
    handler: ChangePhoneHandler = Depends(get_change_phone_handler)
):
    command = ChangePhoneCommand(user_id=user_id, new_phone=request.new_phone_number)
    handler.execute(command)