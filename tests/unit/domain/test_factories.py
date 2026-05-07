import pytest
from unittest.mock import MagicMock
from app.domain.factories.user_factory import UserFactory
from app.domain.factories.todo_factory import TodoFactory
from app.domain.repositories.user_repo import IUserRepository
from app.domain.errors import UserAlreadyExistsError, DomainValidationError
from app.domain.value_objects.priority import Priority

class TestDomainFactories:
    def test_create_user_success(self):
        repo_mock = MagicMock(spec=IUserRepository)
        repo_mock.get_by_email.return_value = None
        factory = UserFactory(repo_mock)

        user = factory.create_user("johndoe", "john@example.com", "John", "Doe", "hashed", "0501234567")
        assert user.username == "johndoe"

    def test_create_user_duplicate_email_raises(self):
        repo_mock = MagicMock(spec=IUserRepository)
        repo_mock.get_by_email.return_value = MagicMock()
        factory = UserFactory(repo_mock)

        with pytest.raises(UserAlreadyExistsError):
            factory.create_user("newuser", "taken@example.com", "N", "U", "hash", "123")

    def test_create_todo_success(self):
        factory = TodoFactory()
        todo = factory.create_todo("Buy groceries", "Milk", 3, 1)
        assert todo.priority == Priority(3)

    def test_create_todo_invalid_priority_raises(self):
        factory = TodoFactory()
        with pytest.raises(DomainValidationError):
            factory.create_todo("Test", "Desc", 10, 1)