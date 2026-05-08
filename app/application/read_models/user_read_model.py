from dataclasses import dataclass

@dataclass(frozen=True)
class UserReadModel:
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    phone_number: str
    role: str