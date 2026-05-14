from dataclasses import dataclass
from app.modules.core.domain.errors import DomainValidationError

@dataclass(frozen=True)
class Priority:
    value: int

    def __post_init__(self):
        if not isinstance(self.value, int):
            raise DomainValidationError("Priority must be an integer")
        
        if self.value < 1 or self.value > 5:
            raise DomainValidationError(f"Priority must be between 1 and 5, got {self.value}")