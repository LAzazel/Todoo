from fastapi import APIRouter, Depends, status
from typing import List
from pydantic import BaseModel

from app.application.commands.admin.delete_user import DeleteUserCommand, DeleteUserHandler
from app.application.queries.admin.get_all_users import GetAllUsersQuery, GetAllUsersHandler

from app.presentation.dependencies import (
    get_admin_get_all_handler, 
    get_admin_delete_user_handler,
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
    handler: GetAllUsersHandler = Depends(get_admin_get_all_handler),
    admin_role: str = Depends(get_current_user_role)
):
    query = GetAllUsersQuery(admin_role=admin_role)
    return handler.execute(query)

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    handler: DeleteUserHandler = Depends(get_admin_delete_user_handler),
    admin_role: str = Depends(get_current_user_role)
):
    command = DeleteUserCommand(user_id=user_id, admin_role=admin_role)
    handler.execute(command)