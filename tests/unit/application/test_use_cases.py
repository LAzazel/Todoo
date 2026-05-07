import pytest
from unittest.mock import MagicMock

from app.application.dto.user_dto import RegisterUserDTO, LoginUserDTO
from app.application.dto.todo_dto import CreateTodoDTO
from app.application.use_cases.auth.register import RegisterUserUseCase
from app.application.use_cases.auth.login import LoginUserUseCase
from app.application.use_cases.todos.create import CreateTodoUseCase
from app.application.use_cases.todos.status import ChangeTodoStatusUseCase
from app.application.use_cases.users.profile import ChangePhoneNumberUseCase
from app.application.use_cases.admin.get_all import AdminGetAllUsersUseCase
from app.domain.errors import UserAlreadyExistsError, InvalidCredentialsError, UnauthorizedAdminAccessError

class TestUseCases:
    def test_register_success(self):
        repo_mock = MagicMock()
        factory_mock = MagicMock()
        hasher_mock = MagicMock()
        
        factory_mock.create_user.return_value = MagicMock(id=1, username="johndoe")
        use_case = RegisterUserUseCase(repo_mock, factory_mock, hasher_mock)
        
        dto = RegisterUserDTO("john@example.com", "pass", "johndoe", "J", "D", "123")
        result = use_case.execute(dto)
        assert result.username == "johndoe"
        repo_mock.add.assert_called_once()

    def test_login_wrong_password_raises(self):
        repo_mock = MagicMock()
        repo_mock.get_by_email.return_value = MagicMock(password_hash="hash1")
        hasher_mock = MagicMock()
        hasher_mock.verify.return_value = False # Паролі не збігаються
        
        use_case = LoginUserUseCase(repo_mock, hasher_mock, MagicMock())
        with pytest.raises(InvalidCredentialsError):
            use_case.execute(LoginUserDTO("john@example.com", "wrongpass"))

    def test_create_todo_success(self):
        repo_mock = MagicMock()
        factory_mock = MagicMock()
        factory_mock.create_todo.return_value = MagicMock(id=1, title="Buy milk")
        
        use_case = CreateTodoUseCase(repo_mock, factory_mock)
        result = use_case.execute(CreateTodoDTO("Buy milk", "Desc", 3), owner_id=1)
        
        assert result.title == "Buy milk"
        repo_mock.add.assert_called_once()

    def test_change_todo_status(self):
        repo_mock = MagicMock()
        todo_mock = MagicMock(owner_id=1)
        repo_mock.get_by_id.return_value = todo_mock
        
        use_case = ChangeTodoStatusUseCase(repo_mock)
        use_case.execute(todo_id=1, owner_id=1, complete=True)
        
        todo_mock.mark_as_completed.assert_called_once()
        repo_mock.update.assert_called_once_with(todo_mock)

    def test_change_phone_success(self):
        repo_mock = MagicMock()
        user_mock = MagicMock()
        repo_mock.get_by_id.return_value = user_mock
        
        use_case = ChangePhoneNumberUseCase(repo_mock)
        use_case.execute(1, "0671112233")
        
        user_mock.update_phone_number.assert_called_once_with("0671112233")

    def test_admin_get_all_non_admin_raises(self):
        use_case = AdminGetAllUsersUseCase(MagicMock())
        with pytest.raises(UnauthorizedAdminAccessError):
            use_case.execute(admin_role="user")