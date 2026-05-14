import pytest
from app.modules.core.domain.models.todo import Todo
from app.modules.core.domain.models.user import User
from app.modules.core.domain.value_objects.email import Email
from app.modules.core.domain.value_objects.priority import Priority
from app.modules.core.domain.errors import DomainValidationError

class TestDomainModels:
    def test_create_todo_success(self):
        todo = Todo(title="Buy milk", description="Store", priority=Priority(3), owner_id=1, complete=False)
        assert todo.title == "Buy milk"
        assert todo.complete is False

    def test_todo_mark_as_completed(self):
        todo = Todo(title="Buy milk", description="Store", priority=Priority(3), owner_id=1, complete=False)
        todo.mark_as_completed()
        assert todo.complete is True

    def test_create_user_success(self):
        user = User(username="johndoe", email=Email("a@a.com"), first_name="A", last_name="B", hashed_password="pw", phone_number="123")
        assert user.username == "johndoe"

    def test_user_short_username_raises(self):
        with pytest.raises(DomainValidationError):
             User(username="ab", email=Email("a@a.com"), first_name="A", last_name="B", hashed_password="pw", phone_number="123")
             
    def test_valid_email(self):
        email = Email("user@example.com")
        assert email.value == "user@example.com"

    def test_invalid_email_no_at(self):
        with pytest.raises(DomainValidationError):
            Email("userexample.com")

    def test_valid_priority_middle(self):
        p = Priority(3)
        assert p.value == 3

    def test_invalid_priority_above_max(self):
        with pytest.raises(DomainValidationError):
            Priority(6)