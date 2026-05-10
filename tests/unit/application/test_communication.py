import pytest
from dataclasses import dataclass, field
from typing import Optional
from unittest.mock import MagicMock

from app.domain.models.todo import Todo
from app.domain.models.user import User
from app.domain.value_objects.email import Email
from app.domain.value_objects.priority import Priority
from app.domain.repositories.todo_repo import ITodoRepository
from app.domain.repositories.user_repo import IUserRepository
from app.domain.factories.todo_factory import TodoFactory
from app.domain.factories.user_factory import UserFactory
from app.domain.errors import TodoNotFoundError, UserNotFoundError

from app.infrastructure.audit.audit_service import InMemoryAuditService
from app.infrastructure.audit.audit_log import AuditLog
from app.infrastructure.event_bus.in_memory_bus import InMemoryEventBus

from app.application.events.todo_events import TodoUpdated
from app.application.events.user_events import (
    UserPasswordChanged,
    UserPhoneChanged,
    UserDeleted,
)
from app.infrastructure.audit.subscribers import (
    on_todo_updated,
    on_user_password_changed,
    on_user_phone_changed,
    on_user_deleted,
)

from app.application.commands.todos.create_todo import CreateTodoCommand, CreateTodoHandler
from app.application.commands.todos.delete_todo import DeleteTodoCommand, DeleteTodoHandler
from app.application.commands.todos.change_status import ChangeTodoStatusCommand, ChangeTodoStatusHandler
from app.application.commands.todos.update_todo import UpdateTodoCommand, UpdateTodoHandler
from app.application.commands.users.change_password import ChangePasswordCommand, ChangePasswordHandler
from app.application.commands.users.change_phone import ChangePhoneCommand, ChangePhoneHandler
from app.application.commands.admin.delete_user import DeleteUserCommand, DeleteUserHandler


class FakeTodoRepository(ITodoRepository):
    def __init__(self, todos: list[Todo] = None):
        self._todos = todos or []
        self._next_id = 1

    def get_by_id(self, todo_id: int) -> Optional[Todo]:
        return next((t for t in self._todos if t.id == todo_id), None)

    def get_all_by_owner_id(self, owner_id: int) -> list[Todo]:
        return [t for t in self._todos if t.owner_id == owner_id]

    def get_all(self) -> list[Todo]:
        return list(self._todos)

    def add(self, todo: Todo) -> None:
        todo.id = self._next_id
        self._next_id += 1
        self._todos.append(todo)

    def update(self, todo: Todo) -> None:
        self._todos = [t if t.id != todo.id else todo for t in self._todos]

    def delete(self, todo: Todo) -> None:
        self._todos = [t for t in self._todos if t.id != todo.id]


class FakeUserRepository(IUserRepository):
    def __init__(self, users: list[User] = None):
        self._users = users or []
        self._next_id = 1

    def get_by_id(self, user_id: int) -> Optional[User]:
        return next((u for u in self._users if u.id == user_id), None)

    def get_by_email(self, email: Email) -> Optional[User]:
        return next((u for u in self._users if u.email == email), None)

    def get_all(self) -> list[User]:
        return list(self._users)

    def add(self, user: User) -> None:
        user.id = self._next_id
        self._next_id += 1
        self._users.append(user)

    def update(self, user: User) -> None:
        self._users = [u if u.id != user.id else user for u in self._users]

    def delete(self, user: User) -> None:
        self._users = [u for u in self._users if u.id != user.id]


def make_todo(owner_id: int = 1) -> Todo:
    todo = Todo(
        title="Buy milk",
        description="From the store",
        priority=Priority(3),
        owner_id=owner_id,
        complete=False,
    )
    todo.id = 1
    return todo


def make_user(user_id: int = 1) -> User:
    user = User(
        username="johndoe",
        email=Email("john@example.com"),
        first_name="John",
        last_name="Doe",
        hashed_password="hashed:secret",
        phone_number="0501234567",
    )
    user.id = user_id
    return user


class TestSyncCommunication:
    def test_create_todo_logs_to_audit(self):
        audit = InMemoryAuditService()
        handler = CreateTodoHandler(FakeTodoRepository(), TodoFactory(), audit)
        handler.execute(CreateTodoCommand(
            title="Buy milk", description="desc", priority=3, owner_id=1
        ))
        logs = audit.get_all()
        assert len(logs) == 1
        assert logs[0].action == "todo_created"
        assert logs[0].user_id == 1
        assert logs[0].details == "Buy milk"

    def test_create_todo_audit_failure_does_not_break_operation(self):
        broken_audit = MagicMock()
        broken_audit.log.side_effect = Exception("audit is down")
        repo = FakeTodoRepository()
        handler = CreateTodoHandler(repo, TodoFactory(), broken_audit)
        result = handler.execute(CreateTodoCommand(
            title="Test", description="desc", priority=1, owner_id=1
        ))
        assert result is not None
        assert len(repo.get_all()) == 1

    def test_delete_todo_logs_to_audit(self):
        audit = InMemoryAuditService()
        todo = make_todo()
        repo = FakeTodoRepository([todo])
        handler = DeleteTodoHandler(repo, audit)
        handler.execute(DeleteTodoCommand(todo_id=1, owner_id=1))
        logs = audit.get_all()
        assert len(logs) == 1
        assert logs[0].action == "todo_deleted"
        assert logs[0].details == "Buy milk"

    def test_delete_todo_not_found_does_not_log(self):
        audit = InMemoryAuditService()
        handler = DeleteTodoHandler(FakeTodoRepository(), audit)
        with pytest.raises(TodoNotFoundError):
            handler.execute(DeleteTodoCommand(todo_id=999, owner_id=1))
        assert len(audit.get_all()) == 0


class TestAsyncCommunication:
    def _make_bus_with_audit(self):
        bus = InMemoryEventBus()
        audit = InMemoryAuditService()
        bus.subscribe(TodoUpdated, on_todo_updated(audit))
        bus.subscribe(UserPasswordChanged, on_user_password_changed(audit))
        bus.subscribe(UserPhoneChanged, on_user_phone_changed(audit))
        bus.subscribe(UserDeleted, on_user_deleted(audit))
        return bus, audit

    def test_update_todo_publishes_event(self):
        bus = InMemoryEventBus()
        received = []
        bus.subscribe(TodoUpdated, lambda e: received.append(e))
        repo = FakeTodoRepository([make_todo()])
        handler = UpdateTodoHandler(repo, bus)
        handler.execute(UpdateTodoCommand(
            todo_id=1, title="New title", description="desc", priority=2, owner_id=1
        ))
        assert len(received) == 1
        assert received[0].new_title == "New title"
        assert received[0].new_priority == 2

    def test_update_todo_audit_receives_via_subscriber(self):
        bus, audit = self._make_bus_with_audit()
        repo = FakeTodoRepository([make_todo()])
        UpdateTodoHandler(repo, bus).execute(UpdateTodoCommand(
            todo_id=1, title="Updated", description="d", priority=4, owner_id=1
        ))
        logs = audit.get_all()
        assert len(logs) == 1
        assert logs[0].action == "todo_updated"
        assert "Updated" in logs[0].details

    def test_change_password_publishes_event(self):
        bus, audit = self._make_bus_with_audit()
        hasher = MagicMock()
        hasher.hash.return_value = "hashed:newpass"
        repo = FakeUserRepository([make_user()])
        ChangePasswordHandler(repo, hasher, bus).execute(
            ChangePasswordCommand(user_id=1, new_password="newpass")
        )
        logs = audit.get_all()
        assert len(logs) == 1
        assert logs[0].action == "user_password_changed"

    def test_delete_user_publishes_event_with_username(self):
        bus, audit = self._make_bus_with_audit()
        repo = FakeUserRepository([make_user()])
        DeleteUserHandler(repo, bus).execute(
            DeleteUserCommand(target_user_id=1, admin_role="admin")
        )
        logs = audit.get_all()
        assert logs[0].action == "user_deleted"
        assert logs[0].details == "johndoe"

    def test_failing_subscriber_does_not_break_other_subscribers(self):
        bus = InMemoryEventBus()
        good_received = []
        bus.subscribe(TodoUpdated, lambda e: (_ for _ in ()).throw(Exception("boom")))
        bus.subscribe(TodoUpdated, lambda e: good_received.append(e))
        repo = FakeTodoRepository([make_todo()])
        UpdateTodoHandler(repo, bus).execute(UpdateTodoCommand(
            todo_id=1, title="X", description="d", priority=1, owner_id=1
        ))
        assert len(good_received) == 1

    def test_no_subscribers_does_not_crash(self):
        bus = InMemoryEventBus()
        repo = FakeTodoRepository([make_todo()])
        handler = UpdateTodoHandler(repo, bus)
        handler.execute(UpdateTodoCommand(
            todo_id=1, title="X", description="d", priority=1, owner_id=1
        ))