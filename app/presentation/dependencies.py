from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.infrastructure.database import get_db
from app.infrastructure.repositories.user_repo import SQLAlchemyUserRepository
from app.infrastructure.repositories.todo_repo import SQLAlchemyTodoRepository
from app.infrastructure.auth.jwt_service import PasslibPasswordHasher, JoseTokenService

from app.domain.factories.user_factory import UserFactory
from app.domain.factories.todo_factory import TodoFactory

from app.application.use_cases.auth.register import RegisterUserUseCase
from app.application.use_cases.auth.login import LoginUserUseCase

from app.application.use_cases.todos.create import CreateTodoUseCase
from app.application.use_cases.todos.get import GetAllUserTodosUseCase, GetTodoUseCase
from app.application.use_cases.todos.update import UpdateTodoUseCase
from app.application.use_cases.todos.delete import DeleteTodoUseCase
from app.application.use_cases.todos.status import ChangeTodoStatusUseCase

from app.application.use_cases.admin.get_all import AdminGetAllUsersUseCase
from app.application.use_cases.admin.delete_user import AdminDeleteUserUseCase

from app.application.use_cases.users.profile import (GetUserProfileUseCase, ChangePasswordUseCase, ChangePhoneNumberUseCase)

from app.config import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_user_repo(db: Session = Depends(get_db)):
    return SQLAlchemyUserRepository(db)

def get_todo_repo(db: Session = Depends(get_db)):
    return SQLAlchemyTodoRepository(db)

def get_password_hasher():
    return PasslibPasswordHasher()

def get_token_service():
    return JoseTokenService()


def get_user_factory(user_repo = Depends(get_user_repo)):
    return UserFactory(user_repo)

def get_todo_factory():
    return TodoFactory()


def get_register_use_case(
    user_repo = Depends(get_user_repo),
    user_factory = Depends(get_user_factory),
    password_hasher = Depends(get_password_hasher)
):
    return RegisterUserUseCase(user_repo, user_factory, password_hasher)

def get_login_use_case(
    user_repo = Depends(get_user_repo),
    password_hasher = Depends(get_password_hasher),
    token_service = Depends(get_token_service)
):
    return LoginUserUseCase(user_repo, password_hasher, token_service)


def get_create_todo_use_case(
    todo_repo = Depends(get_todo_repo),
    todo_factory = Depends(get_todo_factory)
):
    return CreateTodoUseCase(todo_repo, todo_factory)

def get_all_user_todos_use_case(todo_repo = Depends(get_todo_repo)):
    return GetAllUserTodosUseCase(todo_repo)

def get_todo_use_case(todo_repo = Depends(get_todo_repo)):
    return GetTodoUseCase(todo_repo)

def get_update_todo_use_case(todo_repo = Depends(get_todo_repo)):
    return UpdateTodoUseCase(todo_repo)

def get_delete_todo_use_case(todo_repo = Depends(get_todo_repo)):
    return DeleteTodoUseCase(todo_repo)

def get_change_todo_status_use_case(todo_repo = Depends(get_todo_repo)):
    return ChangeTodoStatusUseCase(todo_repo)

def get_admin_get_all_use_case(user_repo = Depends(get_user_repo)):
    return AdminGetAllUsersUseCase(user_repo)

def get_admin_delete_use_case(user_repo = Depends(get_user_repo)):
    return AdminDeleteUserUseCase(user_repo)


def get_user_profile_use_case(user_repo = Depends(get_user_repo)):
    return GetUserProfileUseCase(user_repo)

def get_change_password_use_case(
    user_repo = Depends(get_user_repo),
    password_hasher = Depends(get_password_hasher)
):
    return ChangePasswordUseCase(user_repo, password_hasher)

def get_change_phone_number_use_case(user_repo = Depends(get_user_repo)):
    return ChangePhoneNumberUseCase(user_repo)


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return int(user_id)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def get_current_user_role(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role: str = payload.get("role")
        if role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return role
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")