import pytest
from app.domain.value_objects.email import Email
from app.domain.value_objects.priority import Priority
from app.domain.errors import DomainValidationError

class TestValueObjects:
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