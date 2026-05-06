from abc import ABC, abstractmethod

class IPasswordHasher(ABC):
    @abstractmethod
    def hash(self, password: str) -> str: pass
    @abstractmethod
    def verify(self, plain: str, hashed: str) -> bool: pass

class ITokenService(ABC):
    @abstractmethod
    def generate_token(self, user_id: int, role: str) -> str: pass

    @abstractmethod
    def decode_token(self, token: str) -> dict: pass