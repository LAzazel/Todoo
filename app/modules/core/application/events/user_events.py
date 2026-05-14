from dataclasses import dataclass
from app.modules.core.application.events.base import DomainEvent


@dataclass(frozen=True, kw_only=True)
class UserRegistered(DomainEvent):
    user_id: int
    username: str
    email: str


@dataclass(frozen=True, kw_only=True)
class UserPasswordChanged(DomainEvent):
    user_id: int


@dataclass(frozen=True, kw_only=True)
class UserPhoneChanged(DomainEvent):
    user_id: int
    new_phone: str


@dataclass(frozen=True, kw_only=True)
class UserDeleted(DomainEvent):
    user_id: int
    username: str