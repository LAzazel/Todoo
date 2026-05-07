from tests.conftest import USER_PAYLOAD, ADMIN_PAYLOAD, TODO_PAYLOAD, register, auth_headers
from app.infrastructure.orm.models import UserORM


def test_register_and_login_success(integration_client):
    reg_response = register(integration_client)
    assert reg_response.status_code == 201

    login_response = integration_client.post(
        "/auth/login",
        json={"email": USER_PAYLOAD["email"], "password": USER_PAYLOAD["password"]}
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


def test_create_todo_success(integration_client):
    register(integration_client)
    headers = auth_headers(integration_client, USER_PAYLOAD["email"], USER_PAYLOAD["password"])
    
    response = integration_client.post("/todos/", json=TODO_PAYLOAD, headers=headers)

    assert response.status_code == 201
    assert response.json()["title"] == TODO_PAYLOAD["title"]

def test_get_todos_unauthenticated(integration_client):
    response = integration_client.get("/todos/")
    assert response.status_code == 401


def test_regular_user_cannot_access_admin(integration_client):
    register(integration_client, USER_PAYLOAD)
    headers = auth_headers(integration_client, USER_PAYLOAD["email"], USER_PAYLOAD["password"])
    
    response = integration_client.get("/admin/users", headers=headers)
    assert response.status_code == 403


def test_admin_get_all_users(integration_client, db_session):
    register(integration_client, USER_PAYLOAD)

    register(integration_client, ADMIN_PAYLOAD)
    
    admin_user = db_session.query(UserORM).filter(UserORM.email == ADMIN_PAYLOAD["email"]).first()
    admin_user.role = "admin"
    db_session.commit()
    
    headers_admin = auth_headers(integration_client, ADMIN_PAYLOAD["email"], ADMIN_PAYLOAD["password"])
    response = integration_client.get("/admin/users", headers=headers_admin)
    
    assert response.status_code == 200
    assert len(response.json()) >= 2


def test_admin_delete_user(integration_client, db_session):
    register(integration_client, USER_PAYLOAD)
    
    register(integration_client, ADMIN_PAYLOAD)
    
    admin_user = db_session.query(UserORM).filter(UserORM.email == ADMIN_PAYLOAD["email"]).first()
    admin_user.role = "admin"
    db_session.commit()
    
    headers_admin = auth_headers(integration_client, ADMIN_PAYLOAD["email"], ADMIN_PAYLOAD["password"])
    
    users_list = integration_client.get("/admin/users", headers=headers_admin).json()
    user_to_delete_id = next(u["id"] for u in users_list if u["email"] == USER_PAYLOAD["email"])
    
    delete_response = integration_client.delete(f"/admin/users/{user_to_delete_id}", headers=headers_admin)
    assert delete_response.status_code == 204
