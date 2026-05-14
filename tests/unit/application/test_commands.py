import pytest
from unittest.mock import MagicMock

from app.modules.core.application.commands.admin.delete_user import DeleteUserCommand, DeleteUserHandler
from app.modules.core.application.commands.users.register_user import RegisterUserCommand, RegisterUserHandler
from app.modules.core.application.commands.todos.create_todo import CreateTodoCommand, CreateTodoHandler
from app.modules.core.application.commands.todos.change_status import ChangeTodoStatusCommand, ChangeTodoStatusHandler
from app.modules.core.application.commands.users.change_phone import ChangePhoneCommand, ChangePhoneHandler

from app.modules.core.domain.errors import UserNotFoundError, InvalidCredentialsError, UnauthorizedAdminAccessError

class TestCommands:
    def test_register_success(self):
        repo_mock = MagicMock()
        factory_mock = MagicMock()
        hasher_mock = MagicMock()
        audit_mock = MagicMock()
        event_bus_mock = MagicMock()
        
        factory_mock.create_user.return_value = MagicMock(id=99, username="johndoe")
        handler = RegisterUserHandler(repo_mock, factory_mock, hasher_mock, audit_mock, event_bus_mock)
        
        command = RegisterUserCommand(email="john@example.com", password="pass", username="johndoe", first_name="J", last_name="D", phone_number="123")
        result_id = handler.execute(command)
        assert result_id == 99
        repo_mock.add.assert_called_once()


    def test_create_todo_success(self):
        repo_mock = MagicMock()
        factory_mock = MagicMock()
        audit_mock = MagicMock()
        event_bus_mock = MagicMock()
        factory_mock.create_todo.return_value = MagicMock(id=5, title="Buy milk")
        
        handler = CreateTodoHandler(repo_mock, factory_mock, audit_mock, event_bus_mock)
        result_id = handler.execute(CreateTodoCommand(title="Buy milk", description="Desc", priority=3, owner_id=1))
        
        assert result_id == 5
        repo_mock.add.assert_called_once()

    def test_change_todo_status(self):
        repo_mock = MagicMock()
        todo_mock = MagicMock(owner_id=1)
        audit_mock = MagicMock()
        event_bus_mock = MagicMock()
        repo_mock.get_by_id.return_value = todo_mock
        
        handler = ChangeTodoStatusHandler(repo_mock, audit_mock, event_bus_mock)
        handler.execute(ChangeTodoStatusCommand(todo_id=1, owner_id=1, complete=True))
        
        todo_mock.mark_as_completed.assert_called_once()
        repo_mock.update.assert_called_once_with(todo_mock)

    def test_change_phone_success(self):
        repo_mock = MagicMock()
        user_mock = MagicMock()
        event_bus_mock = MagicMock()
        repo_mock.get_by_id.return_value = user_mock
        
        handler = ChangePhoneHandler(repo_mock, event_bus_mock)
        handler.execute(ChangePhoneCommand(user_id=1, new_phone="0671112233"))
        
        user_mock.update_phone_number.assert_called_once_with("0671112233")
        repo_mock.update.assert_called_once_with(user_mock)

    def test_admin_delete_user_success(self):
        repo_mock = MagicMock()
        user_mock = MagicMock(id=5)
        event_bus_mock = MagicMock()
        repo_mock.get_by_id.return_value = user_mock
        
        handler = DeleteUserHandler(repo_mock, event_bus_mock)
        handler.execute(DeleteUserCommand(target_user_id=5, admin_role="admin"))
        
        repo_mock.delete.assert_called_once_with(user_mock)

    def test_admin_delete_user_not_found_raises(self):
        repo_mock = MagicMock()
        event_bus_mock = MagicMock()
        repo_mock.get_by_id.return_value = None
        
        handler = DeleteUserHandler(repo_mock, event_bus_mock)
        
        with pytest.raises(UserNotFoundError):
            handler.execute(DeleteUserCommand(target_user_id=999, admin_role="admin"))

    def test_admin_delete_non_admin_raises(self):
        repo_mock = MagicMock()
        event_bus_mock = MagicMock()
        
        handler = DeleteUserHandler(repo_mock, event_bus_mock)
        command = DeleteUserCommand(target_user_id=5, admin_role="user")
        
        with pytest.raises(UnauthorizedAdminAccessError):
            handler.execute(command)