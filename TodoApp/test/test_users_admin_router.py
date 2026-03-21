from types import SimpleNamespace

from starlette import status


def test_admin_read_all_todos_returns_403_for_non_admin(client, set_current_user):
    set_current_user({"id": 1, "username": "john", "role": "user"})

    response = client.get("/admin/todo")

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Not enough permissions"


def test_change_password_returns_404_when_user_not_found(client, mock_db, set_current_user):
    set_current_user({"id": 1, "username": "john", "role": "user"})
    mock_db.query.return_value.filter.return_value.first.return_value = None

    response = client.put("/user/change_password", json="new-password")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"


def test_change_phone_number_updates_value_and_returns_204(client, mock_db, set_current_user):
    set_current_user({"id": 1, "username": "john", "role": "user"})
    user_model = SimpleNamespace(phone_number="1111111111", hashed_password="old")
    mock_db.query.return_value.filter.return_value.first.return_value = user_model

    response = client.put("/user/change_phone_number", json="1234567890")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert user_model.phone_number == "1234567890"
    mock_db.commit.assert_called_once()

