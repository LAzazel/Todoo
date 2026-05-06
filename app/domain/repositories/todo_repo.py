from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.models.todo import Todo


class ITodoRepository(ABC):
    @abstractmethod
    def get_by_id(self, todo_id: int) -> Optional[Todo]:
        pass

    @abstractmethod
    def get_all_by_user_id(self, user_id: int) -> List[Todo]:
        pass

    @abstractmethod
    def add(self, todo: Todo) -> None:
        pass