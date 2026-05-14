from abc import ABC, abstractmethod
from typing import Optional, List
from app.modules.core.domain.models.todo import Todo


class ITodoRepository(ABC):
    @abstractmethod
    def get_by_id(self, todo_id: int) -> Optional[Todo]:
        pass

    @abstractmethod
    def get_all_by_owner_id(self, owner_id: int) -> List[Todo]:
        pass

    @abstractmethod
    def get_all(self) -> List[Todo]:
        pass

    @abstractmethod
    def add(self, todo: Todo) -> None:
        pass

    @abstractmethod
    def update(self, todo: Todo) -> None:
        pass

    @abstractmethod
    def delete(self, todo: Todo) -> None:
        pass