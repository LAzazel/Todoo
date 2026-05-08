from dataclasses import dataclass
from app.application.events.base import DomainEvent


@dataclass(frozen=True)
class UserRegistered(DomainEvent):
    user_id: int
    username: str
    email: str


@dataclass(frozen=True)
class UserPasswordChanged(DomainEvent):
    user_id: int


@dataclass(frozen=True)
class UserDeleted(DomainEvent):
    user_id: int
    username: str