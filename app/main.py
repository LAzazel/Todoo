from fastapi import FastAPI
from app.infrastructure.database import engine, Base

from app.presentation.routers import auth, todos, users, admin

from app.domain import errors
from app.presentation.error_handler import domain_error_exception_handler

from app.application.events.user_events import UserPhoneChanged, UserPasswordChanged, UserDeleted
from app.application.events.todo_events import TodoUpdated
from app.infrastructure.audit.subscribers import on_user_phone_changed, on_user_password_changed, on_user_deleted, on_todo_updated
from app.presentation.dependencies import _audit_service, _event_bus

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