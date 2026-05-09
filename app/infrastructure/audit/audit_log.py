from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AuditLog:
    user_id: int
    action: str
    entity_id: int
    occurred_at: datetime = field(default_factory=datetime.now)
    details: str = ""