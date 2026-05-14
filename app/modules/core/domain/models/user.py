from dataclasses import dataclass
from typing import Optional
from app.modules.core.domain.value_objects.email import Email
from app.modules.core.domain.errors import DomainValidationError


@dataclass
class User:
    username: str
    email: Email
    first_name: str
    last_name: str
    hashed_password: str
    phone_number: str
    role: str = "user"
    is_active: bool = True
    id: Optional[int] = None

    def __post_init__(self):
        if not self.username.strip():
            raise DomainValidationError("Username cannot be empty")
        if len(self.username) < 3:
            raise DomainValidationError("Username must be at least 3 characters long")

    
    def change_password(self, new_hashed_password: str) -> None:
        if not new_hashed_password:
            raise DomainValidationError("Password hash cannot be empty")
        self.hashed_password = new_hashed_password

    def update_phone_number(self, new_phone: str) -> None:
        if not new_phone.strip():
            raise DomainValidationError("Phone number cannot be empty")
        self.phone_number = new_phone