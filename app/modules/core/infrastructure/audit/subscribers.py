from app.modules.core.application.events.todo_events import TodoUpdated
from app.modules.core.application.events.user_events import (
    UserPasswordChanged,
    UserPhoneChanged,
    UserDeleted,
)
from app.modules.core.infrastructure.audit.interfaces import IAuditService
from app.modules.core.infrastructure.audit.audit_log import AuditLog


def on_todo_updated(audit: IAuditService):
    def handler(event: TodoUpdated) -> None:
        audit.log(AuditLog(
            user_id=event.owner_id,
            action="todo_updated",
            entity_id=event.todo_id,
            details=f"new_title={event.new_title}, new_priority={event.new_priority}",
        ))
    return handler


def on_user_password_changed(audit: IAuditService):
    def handler(event: UserPasswordChanged) -> None:
        audit.log(AuditLog(
            user_id=event.user_id,
            action="user_password_changed",
            entity_id=event.user_id,
        ))
    return handler


def on_user_phone_changed(audit: IAuditService):
    def handler(event: UserPhoneChanged) -> None:
        audit.log(AuditLog(
            user_id=event.user_id,
            action="user_phone_changed",
            entity_id=event.user_id,
            details=event.new_phone,
        ))
    return handler


def on_user_deleted(audit: IAuditService):
    def handler(event: UserDeleted) -> None:
        audit.log(AuditLog(
            user_id=event.user_id,
            action="user_deleted",
            entity_id=event.user_id,
            details=event.username,
        ))
    return handler