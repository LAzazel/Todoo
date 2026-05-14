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
from app.modules.core.public_contract import TodoCreatedIntegrationEvent, TodoCompletedIntegrationEvent, UserRegisteredIntegrationEvent

from app.modules.analytics.infrastructure.acl import AnalyticsACL
from app.modules.analytics.application.handlers import AnalyticsHandlers
from app.modules.analytics.presentation.routers import router as analytics_router
from app.modules.analytics.public_contract import get_stats_store

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todoo API", description="A simple To-Do application with layered architecture", version="1.0.0")

app.add_exception_handler(errors.DomainError, domain_error_exception_handler)

analytics_handlers = AnalyticsHandlers(get_stats_store())
analytics_acl = AnalyticsACL(analytics_handlers)

_event_bus.subscribe(TodoUpdated, on_todo_updated(_audit_service))
_event_bus.subscribe(UserPasswordChanged, on_user_password_changed(_audit_service))
_event_bus.subscribe(UserPhoneChanged, on_user_phone_changed(_audit_service))
_event_bus.subscribe(UserDeleted, on_user_deleted(_audit_service))
_event_bus.subscribe(TodoCreatedIntegrationEvent, analytics_acl.translate_and_handle_created)
_event_bus.subscribe(TodoCompletedIntegrationEvent, analytics_acl.translate_and_handle_completed)
_event_bus.subscribe(UserRegisteredIntegrationEvent, analytics_acl.translate_and_handle_user_registered)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(analytics_router)

@app.get("/")
def root():
    return {"message": "Welcome to Todoo API"}