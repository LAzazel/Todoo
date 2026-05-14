from dataclasses import dataclass
from app.modules.core.application.events.base import DomainEvent


@dataclass(frozen=True, kw_only=True)
class TodoCreated(DomainEvent):
    todo_id: int
    owner_id: int
    title: str
    description: str
    priority: int


@dataclass(frozen=True, kw_only=True)
class TodoDeleted(DomainEvent):
    todo_id: int
    owner_id: int
    title: str


@dataclass(frozen=True, kw_only=True)
class TodoStatusChanged(DomainEvent):
    todo_id: int
    owner_id: int
    complete: bool


@dataclass(frozen=True, kw_only=True)
class TodoUpdated(DomainEvent):
    todo_id: int
    owner_id: int
    new_title: str
    new_priority: int