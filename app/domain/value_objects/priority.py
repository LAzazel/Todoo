from dataclasses import dataclass
from app.domain.errors import ValidationError

@dataclass(frozen=True)
class Priority:
    value: int

    def __post_init__(self):
        if not isinstance(self.value, int):
            raise ValidationError("Priority must be an integer")
        
        if self.value < 1 or self.value > 5:
            raise ValidationError(f"Priority must be between 1 and 5, got {self.value}")