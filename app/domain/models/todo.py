from dataclasses import dataclass
from typing import Optional
from app.domain.value_objects.priority import Priority
from app.domain.errors import DomainValidationError


@dataclass
class Todo:
    title: str
    description: str
    priority: Priority
    owner_id: int
    complete: bool = False
    id: Optional[int] = None

    def __post_init__(self):
        if not self.title.strip():
            raise DomainValidationError("Todo title cannot be empty")
        if self.owner_id <= 0:
            raise DomainValidationError("Invalid owner ID")


    def mark_as_completed(self) -> None:
        self.complete = True

    def mark_as_incomplete(self) -> None:
        self.complete = False

    def update_details(self, title: str, description: str, priority: Priority) -> None:
        if not title.strip():
            raise DomainValidationError("Todo title cannot be empty")
        self.title = title
        self.description = description
        self.priority = priority