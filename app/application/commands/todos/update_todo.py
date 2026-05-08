from dataclasses import dataclass
from app.domain.errors import TodoNotFoundError
from app.domain.repositories.todo_repo import ITodoRepository
from app.domain.value_objects import Priority



@dataclass(frozen=True)
class UpdateTodoCommand:
    todo_id: int
    title: str
    description: str
    priority: int
    owner_id: int

class UpdateTodoHandler:
    def __init__(self, todo_repo: ITodoRepository):
        self.todo_repo = todo_repo

    def execute(self, command: UpdateTodoCommand) -> None:
        todo = self.todo_repo.get_by_id(command.todo_id)
        if not todo or todo.owner_id != command.owner_id:
            raise TodoNotFoundError("Todo not found or you don't have access to it.")

        new_priority = Priority(command.priority)
        todo.update_details(title=command.title, description=command.description, priority=new_priority)
        
        self.todo_repo.update(todo)