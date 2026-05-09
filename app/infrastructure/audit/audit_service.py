from app.infrastructure.audit.interfaces import IAuditService
from app.infrastructure.audit.audit_log import AuditLog


class InMemoryAuditService(IAuditService):
    def __init__(self):
        self._logs: list[AuditLog] = []

    def log(self, entry: AuditLog) -> None:
        self._logs.append(entry)

    def get_all(self) -> list[AuditLog]:
        return list(self._logs)

    def get_by_user(self, user_id: int) -> list[AuditLog]:
        return [log for log in self._logs if log.user_id == user_id]