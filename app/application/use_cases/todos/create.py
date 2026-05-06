from app.application.dto.todo_dto import CreateTodoDTO, TodoResponseDTO
from app.domain.factories.todo_factory import TodoFactory
from app.domain.repositories.todo_repo import ITodoRepository

class CreateTodoUseCase:
    def __init__(self, todo_repo: ITodoRepository, todo_factory: TodoFactory):
        self.todo_repo = todo_repo
        self.todo_factory = todo_factory

    def execute(self, dto: CreateTodoDTO, user_id: int) -> TodoResponseDTO:
        todo = self.todo_factory.create_todo(
            title=dto.title,
            description=dto.description,
            priority_val=dto.priority,
            user_id=user_id
        )

        self.todo_repo.add(todo)

        return TodoResponseDTO(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            priority=todo.priority.value,
            user_id=todo.user_id
        )