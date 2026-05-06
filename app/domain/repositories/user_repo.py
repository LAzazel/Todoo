from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models.user import User
from app.domain.value_objects.email import Email


class IUserRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: Email) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def add(self, user: User) -> None:
        pass