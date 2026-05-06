from fastapi import APIRouter, Depends, status
from typing import List
from pydantic import BaseModel

from app.application.use_cases.admin.get_all import AdminGetAllUsersUseCase
from app.application.use_cases.admin.delete_user import AdminDeleteUserUseCase
from app.presentation.dependencies import (
    get_admin_get_all_use_case, 
    get_admin_delete_use_case,
    get_current_user_role
)


router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


class UserResponse(BaseModel):
    id: int
    email: str

@router.get("/users", response_model=List[UserResponse])
def get_users(
    use_case: AdminGetAllUsersUseCase = Depends(get_admin_get_all_use_case),
    admin_role: str = Depends(get_current_user_role)
):
    return use_case.execute(admin_role)

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    use_case: AdminDeleteUserUseCase = Depends(get_admin_delete_use_case),
    admin_role: str = Depends(get_current_user_role)
):
    use_case.execute(user_id, admin_role)