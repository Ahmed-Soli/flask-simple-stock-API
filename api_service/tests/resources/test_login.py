import json


def test_login(test_client):
    login_data = {"username": "admin", "password": "admin"}
    response = test_client.post(
        "/api/v1/login",
        data=json.dumps(login_data),
        headers={"Content-Type": "application/json"},
    )
    json_data = response.get_json()

    assert response.status_code == 200
    assert "token" in json_data


def test_invalid_login(test_client):
    login_data = {"username": "test", "password": "test"}
    response = test_client.post(
        "/api/v1/login",
        data=json.dumps(login_data),
        headers={"Content-Type": "application/json"},
    )

    assert b"Invalid user credentials" in response.data
    assert response.status_code == 401
