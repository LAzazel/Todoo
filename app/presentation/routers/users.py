from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field

from app.application.use_cases.users.profile import (
    GetUserProfileUseCase,
    ChangePasswordUseCase,
    ChangePhoneNumberUseCase
)
from app.presentation.dependencies import (
    get_current_user_id,
    get_user_profile_use_case,
    get_change_password_use_case,
    get_change_phone_number_use_case
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
    use_case: GetUserProfileUseCase = Depends(get_user_profile_use_case)
):
    return use_case.execute(user_id)

@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(
    request: ChangePasswordRequest,
    user_id: int = Depends(get_current_user_id),
    use_case: ChangePasswordUseCase = Depends(get_change_password_use_case)
):
    use_case.execute(user_id, request.new_password)

@router.put("/change_phone_number", status_code=status.HTTP_204_NO_CONTENT)
def change_phone_number(
    request: ChangePhoneNumberRequest,
    user_id: int = Depends(get_current_user_id),
    use_case: ChangePhoneNumberUseCase = Depends(get_change_phone_number_use_case)
):
    use_case.execute(user_id, request.new_phone_number)