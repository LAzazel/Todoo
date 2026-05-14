from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app.modules.core.application.interfaces.auth_services import ITokenService
from app.modules.core.domain.errors import InvalidCredentialsError

from app.modules.core.infrastructure.audit.audit_service import InMemoryAuditService
from app.modules.core.infrastructure.database import get_db
from app.modules.core.infrastructure.repositories.user_repo import SQLAlchemyUserRepository
from app.modules.core.infrastructure.repositories.todo_repo import SQLAlchemyTodoRepository
from app.modules.core.infrastructure.auth.jwt_service import PasslibPasswordHasher, JoseTokenService
from app.modules.core.infrastructure.audit.interfaces import IAuditService
from app.modules.core.infrastructure.event_bus.interfaces import IEventBus
from app.modules.core.infrastructure.event_bus.in_memory_bus import InMemoryEventBus

from app.modules.core.domain.factories.user_factory import UserFactory
from app.modules.core.domain.factories.todo_factory import TodoFactory

#sync handlers
from app.modules.core.application.commands.users.register_user import RegisterUserHandler
from app.modules.core.application.commands.todos.create_todo import CreateTodoHandler
from app.modules.core.application.commands.todos.delete_todo import DeleteTodoHandler
from app.modules.core.application.commands.todos.change_status import ChangeTodoStatusHandler

#async handlers
from app.modules.core.application.commands.todos.update_todo import UpdateTodoHandler
from app.modules.core.application.commands.users.change_password import ChangePasswordHandler
from app.modules.core.application.commands.users.change_phone import ChangePhoneHandler
from app.modules.core.application.commands.admin.delete_user import DeleteUserHandler

from app.modules.core.application.queries.auth.login import LoginHandler
from app.modules.core.application.queries.todos.get_todo import GetTodoHandler
from app.modules.core.application.queries.todos.get_all_todos import GetAllTodosHandler
from app.modules.core.application.queries.users.get_profile import GetProfileHandler
from app.modules.core.application.queries.admin.get_all_users import GetAllUsersHandler

from app.config import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

_audit_service = InMemoryAuditService()
_event_bus = InMemoryEventBus()


def get_user_repo(db: Session = Depends(get_db)):
    return SQLAlchemyUserRepository(db)

def get_todo_repo(db: Session = Depends(get_db)):
    return SQLAlchemyTodoRepository(db)

def get_password_hasher():
    return PasslibPasswordHasher()

def get_token_service():
    return JoseTokenService()

def get_audit_service() -> IAuditService:
    return _audit_service

def get_event_bus() -> IEventBus:
    return _event_bus


def get_user_factory(user_repo = Depends(get_user_repo)):
    return UserFactory(user_repo)

def get_todo_factory():
    return TodoFactory()


def get_register_handler(user_repo=Depends(get_user_repo), factory=Depends(get_user_factory), hasher=Depends(get_password_hasher), audit_service=Depends(get_audit_service)):
    return RegisterUserHandler(user_repo, factory, hasher, audit_service)

def get_create_todo_handler(repo=Depends(get_todo_repo), factory=Depends(get_todo_factory), audit_service=Depends(get_audit_service), event_bus=Depends(get_event_bus)):
    return CreateTodoHandler(repo, factory, audit_service, event_bus)

def get_update_todo_handler(repo=Depends(get_todo_repo), event_bus=Depends(get_event_bus)): return UpdateTodoHandler(repo, event_bus)
def get_delete_todo_handler(repo=Depends(get_todo_repo), audit_service=Depends(get_audit_service)): return DeleteTodoHandler(repo, audit_service)
def get_change_status_handler(repo=Depends(get_todo_repo), audit_service=Depends(get_audit_service)): return ChangeTodoStatusHandler(repo, audit_service)

def get_change_password_handler(repo=Depends(get_user_repo), hasher=Depends(get_password_hasher), event_bus=Depends(get_event_bus)):
    return ChangePasswordHandler(repo, hasher, event_bus)

def get_change_phone_handler(repo=Depends(get_user_repo), event_bus=Depends(get_event_bus)): return ChangePhoneHandler(repo, event_bus)
def get_admin_delete_user_handler(repo=Depends(get_user_repo), event_bus=Depends(get_event_bus)): return DeleteUserHandler(repo, event_bus)


def get_login_handler(repo=Depends(get_user_repo), hasher=Depends(get_password_hasher), token_svc=Depends(get_token_service)):
    return LoginHandler(repo, hasher, token_svc)

def get_todo_handler(repo=Depends(get_todo_repo)): return GetTodoHandler(repo)
def get_all_todos_handler(repo=Depends(get_todo_repo)): return GetAllTodosHandler(repo)
def get_profile_handler(repo=Depends(get_user_repo)): return GetProfileHandler(repo)
def get_admin_get_all_handler(repo=Depends(get_user_repo)): return GetAllUsersHandler(repo)


def get_current_user_id(
    token: str = Depends(oauth2_scheme),
    token_service: ITokenService = Depends(get_token_service)
) -> int:
    try:
        payload = token_service.decode_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return int(user_id)
    except InvalidCredentialsError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user_role(
    token: str = Depends(oauth2_scheme),
    token_service: ITokenService = Depends(get_token_service)
) -> str:
    try:
        payload = token_service.decode_token(token)
        role = payload.get("role")
        if role is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return role
    except InvalidCredentialsError:
        raise HTTPException(status_code=401, detail="Invalid token")