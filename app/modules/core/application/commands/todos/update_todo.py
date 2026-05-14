from dataclasses import dataclass
from app.modules.core.domain.errors import TodoNotFoundError
from app.modules.core.domain.repositories.todo_repo import ITodoRepository
from app.modules.core.domain.value_objects.priority import Priority
from app.modules.core.infrastructure.event_bus.interfaces import IEventBus
from app.modules.core.application.events.todo_events import TodoUpdated



@dataclass(frozen=True)
class UpdateTodoCommand:
    todo_id: int
    title: str
    description: str
    priority: int
    owner_id: int

class UpdateTodoHandler:
    def __init__(self, todo_repo: ITodoRepository, event_bus: IEventBus):
        self.todo_repo = todo_repo
        self.event_bus = event_bus

    def execute(self, command: UpdateTodoCommand) -> None:
        todo = self.todo_repo.get_by_id(command.todo_id)
        if not todo or todo.owner_id != command.owner_id:
            raise TodoNotFoundError("Todo not found or you don't have access to it.")

        new_priority = Priority(command.priority)
        todo.update_details(title=command.title, description=command.description, priority=new_priority)
        
        self.todo_repo.update(todo)

        self.event_bus.publish(TodoUpdated(
            todo_id=command.todo_id,
            owner_id=command.owner_id,
            new_title=command.title,
            new_priority=command.priority
        ))