from abc import ABC, abstractmethod
from app.infrastructure.audit.audit_log import AuditLog


class IAuditService(ABC):
    @abstractmethod
    def log(self, entry: AuditLog) -> None: pass

    @abstractmethod
    def get_all(self) -> list[AuditLog]: pass

    @abstractmethod
    def get_by_user(self, user_id: int) -> list[AuditLog]: pass