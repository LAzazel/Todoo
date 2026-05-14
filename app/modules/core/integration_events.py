from dataclasses import dataclass, field
from datetime import datetime

@dataclass(kw_only=True)
class IntegrationEvent:
    occurred_on: datetime = field(default_factory=datetime.utcnow)

@dataclass(kw_only=True)
class TodoCreatedIntegrationEvent(IntegrationEvent):
    todo_id: int
    owner_id: int
    priority: int

@dataclass(kw_only=True)
class TodoCompletedIntegrationEvent(IntegrationEvent):
    todo_id: int
    owner_id: int

@dataclass(kw_only=True)
class UserRegisteredIntegrationEvent(IntegrationEvent):
    user_id: int
    email: str