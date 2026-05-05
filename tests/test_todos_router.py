from starlette import status


def test_read_all_todos_unauthenticated(client, set_current_user):
    set_current_user(None)

    response = client.get("/todos/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Authentication failed"


def test_read_todo_not_found(client, mock_db, set_current_user):
    set_current_user({"id": 1, "username": "john", "role": "user"})
    mock_db.query.return_value.filter.return_value.filter.return_value.first.return_value = None

    response = client.get("/todos/1")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Todo not found"


def test_create_todo_success(client, mock_db, set_current_user):
    set_current_user({"id": 3, "username": "john", "role": "user"})
    payload = {
        "title": "Buy milk",
        "description": "From local store",
        "priority": 3,
        "complete": False,
    }

    response = client.post("/todos/create_todo", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()

    created_todo = mock_db.add.call_args.args[0]
    assert created_todo.owner_id == 3
    assert created_todo.title == payload["title"]

