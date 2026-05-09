from dataclasses import dataclass
from app.domain.errors import TodoNotFoundError
from app.domain.repositories.todo_repo import ITodoRepository
from app.infrastructure.audit.audit_log import AuditLog
from app.infrastructure.audit.interfaces import IAuditService


@dataclass(frozen=True)
class ChangeTodoStatusCommand:
    todo_id: int
    owner_id: int
    complete: bool

class ChangeTodoStatusHandler:
    def __init__(self, todo_repo: ITodoRepository, audit_service: IAuditService):
        self.todo_repo = todo_repo
        self.audit_service = audit_service

    def execute(self, command: ChangeTodoStatusCommand) -> None:
        todo = self.todo_repo.get_by_id(command.todo_id)
        if not todo or todo.owner_id != command.owner_id:
            raise TodoNotFoundError("Todo not found or you don't have access to it.")

        if command.complete:
            todo.mark_as_completed()
        else:
            todo.mark_as_incomplete()
            
        self.todo_repo.update(todo)

        try:
            status_str = "completed" if command.complete else "reopened"
            self.audit_service.log(AuditLog(
                user_id=command.owner_id,
                action=f"todo_{status_str}",
                entity_id=command.todo_id,
                details=todo.title
            ))
        except Exception:
            pass