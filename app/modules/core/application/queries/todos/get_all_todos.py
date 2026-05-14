from dataclasses import dataclass
from typing import List
from app.modules.core.domain.repositories.todo_repo import ITodoRepository
from app.modules.core.application.read_models.todo_read_model import TodoReadModel


@dataclass(frozen=True)
class GetAllTodosQuery:
    owner_id: int

class GetAllTodosHandler:
    def __init__(self, todo_repo: ITodoRepository):
        self.todo_repo = todo_repo

    def execute(self, query: GetAllTodosQuery) -> List[TodoReadModel]:
        todos = self.todo_repo.get_all_by_owner_id(query.owner_id)
        
        return [
            TodoReadModel(
                id=todo.id,
                title=todo.title,
                description=todo.description,
                priority=todo.priority.value,
                owner_id=todo.owner_id,
                complete=todo.complete
            ) for todo in todos
        ]