from tests.conftest import USER_PAYLOAD, ADMIN_PAYLOAD, TODO_PAYLOAD, register, auth_headers


def test_register_and_login_success(integration_client):
    reg_response = register(integration_client)
    assert reg_response.status_code == 201

    login_response = integration_client.post(
        "/auth/token",
        data={"username": USER_PAYLOAD["username"], "password": USER_PAYLOAD["password"]}
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


def test_create_todo_success(integration_client):
    register(integration_client)
    headers = auth_headers(integration_client, USER_PAYLOAD["username"], USER_PAYLOAD["password"])
    
    response = integration_client.post("/todos/", json=TODO_PAYLOAD, headers=headers)
    
    assert response.status_code == 201


def test_get_todos_unauthenticated(integration_client):
    response = integration_client.get("/todos/")
    assert response.status_code == 401


def test_regular_user_cannot_access_admin(integration_client):
    register(integration_client)
    headers = auth_headers(integration_client, USER_PAYLOAD["username"], USER_PAYLOAD["password"])
    
    response = integration_client.get("/admin/todo", headers=headers)
    
    assert response.status_code == 403


def test_admin_get_all_todos(integration_client):
    register(integration_client, USER_PAYLOAD)
    headers_user = auth_headers(integration_client, USER_PAYLOAD["username"], USER_PAYLOAD["password"])
    integration_client.post("/todos/", json=TODO_PAYLOAD, headers=headers_user)

    register(integration_client, ADMIN_PAYLOAD)
    headers_admin = auth_headers(integration_client, ADMIN_PAYLOAD["username"], ADMIN_PAYLOAD["password"])
    
    response = integration_client.get("/admin/todo", headers=headers_admin)
    
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_admin_delete_todo(integration_client):
    register(integration_client, USER_PAYLOAD)
    headers_user = auth_headers(integration_client, USER_PAYLOAD["username"], USER_PAYLOAD["password"])
    integration_client.post("/todos/", json=TODO_PAYLOAD, headers=headers_user)
    
    todo_id = integration_client.get("/todos/", headers=headers_user).json()[0]["id"]

    register(integration_client, ADMIN_PAYLOAD)
    headers_admin = auth_headers(integration_client, ADMIN_PAYLOAD["username"], ADMIN_PAYLOAD["password"])
    
    delete_response = integration_client.delete(f"/admin/todo/{todo_id}", headers=headers_admin)
    assert delete_response.status_code == 204

    check_response = integration_client.get(f"/todos/{todo_id}", headers=headers_user)
    assert check_response.status_code == 404


def test_admin_delete_todo_not_found(integration_client):
    register(integration_client, ADMIN_PAYLOAD)
    headers_admin = auth_headers(integration_client, ADMIN_PAYLOAD["username"], ADMIN_PAYLOAD["password"])
    
    response = integration_client.delete("/admin/todo/999", headers=headers_admin)
    
    assert response.status_code == 404