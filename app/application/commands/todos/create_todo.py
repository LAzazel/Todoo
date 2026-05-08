from dataclasses import dataclass
from app.domain.factories.todo_factory import TodoFactory
from app.domain.repositories.todo_repo import ITodoRepository


@dataclass(frozen=True)
class CreateTodoCommand:
    title: str
    description: str
    priority: int
    owner_id: int

class CreateTodoHandler:
    def __init__(self, todo_repo: ITodoRepository, todo_factory: TodoFactory):
        self.todo_repo = todo_repo
        self.todo_factory = todo_factory

    def execute(self, command: CreateTodoCommand) -> int:
        todo = self.todo_factory.create_todo(
            title=command.title,
            description=command.description,
            priority_val=command.priority,
            owner_id=command.owner_id
        )
        self.todo_repo.add(todo)
        return todo.id