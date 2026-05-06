from dataclasses import dataclass

@dataclass(frozen=True)
class RegisterUserDTO:
    email: str
    password: str
    username: str
    first_name: str
    last_name: str
    phone_number: str

@dataclass(frozen=True)
class LoginUserDTO:
    email: str
    password: str

@dataclass(frozen=True)
class UserResponseDTO:
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    phone_number: str
    role: str