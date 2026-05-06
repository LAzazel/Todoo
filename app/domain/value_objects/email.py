import re
from dataclasses import dataclass
from app.domain.errors import DomainValidationError

EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if not self.value or not isinstance(self.value, str):
            raise DomainValidationError("Email cannot be empty")
        
        if not EMAIL_REGEX.match(self.value):
            raise DomainValidationError(f"Invalid email format: {self.value}")