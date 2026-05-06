from app.application.dto.todo_dto import UpdateTodoDTO, TodoResponseDTO
from app.domain.repositories.todo_repo import ITodoRepository
from app.domain.errors import TodoNotFoundError
from app.domain.value_objects.priority import Priority


class UpdateTodoUseCase:
    def __init__(self, todo_repo: ITodoRepository):
        self.todo_repo = todo_repo

    def execute(self, todo_id: int, dto: UpdateTodoDTO, owner_id: int) -> TodoResponseDTO:
        todo = self.todo_repo.get_by_id(todo_id)
        
        if not todo or todo.owner_id != owner_id:
            raise TodoNotFoundError("Todo not found or you don't have access to it")

        new_priority = Priority(dto.priority)
        todo.update_details(title=dto.title, description=dto.description, priority=new_priority)

        self.todo_repo.update(todo)

        return TodoResponseDTO(
            id=todo.id, title=todo.title, description=todo.description, 
            priority=todo.priority.value, owner_id=todo.owner_id, complete=todo.complete
        )