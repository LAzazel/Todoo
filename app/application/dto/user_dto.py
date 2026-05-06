from dataclasses import dataclass

@dataclass(frozen=True)
class RegisterUserDTO:
    email: str
    password: str

@dataclass(frozen=True)
class LoginUserDTO:
    email: str
    password: str

@dataclass(frozen=True)
class UserResponseDTO:
    id: int
    email: str