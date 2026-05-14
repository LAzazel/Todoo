from fastapi import FastAPI
from app.modules.core.infrastructure.database import engine, Base

from app.modules.core.presentation.routers import admin, auth, todos
from app.modules.core.presentation.routers import users

from app.modules.core.domain import errors
from app.modules.core.presentation.error_handler import domain_error_exception_handler

from app.modules.core.application.events.user_events import UserPhoneChanged, UserPasswordChanged, UserDeleted
from app.modules.core.application.events.todo_events import TodoUpdated
from app.modules.core.infrastructure.audit.subscribers import on_user_phone_changed, on_user_password_changed, on_user_deleted, on_todo_updated
from app.modules.core.presentation.dependencies import _audit_service, _event_bus

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todoo API", description="A simple To-Do application with layered architecture", version="1.0.0")

app.add_exception_handler(errors.DomainError, domain_error_exception_handler)

_event_bus.subscribe(TodoUpdated, on_todo_updated(_audit_service))
_event_bus.subscribe(UserPasswordChanged, on_user_password_changed(_audit_service))
_event_bus.subscribe(UserPhoneChanged, on_user_phone_changed(_audit_service))
_event_bus.subscribe(UserDeleted, on_user_deleted(_audit_service))

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {"message": "Welcome to Todoo API"}