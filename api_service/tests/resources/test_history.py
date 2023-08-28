from api_service.models import StockCall


def test_history(test_client, db, user_token):
    db.session.query(StockCall).delete()
    db.session.commit()

    response = test_client.get(
        "/api/v1/users/history",
        headers={"Authorization": "Bearer {}".format(user_token)},
    )
    assert len(response.get_json()) == 0
    assert response.status_code == 200

    fake_stock_data = {
        "time": "20:33:45",
        "high": 13.42,
        "name": "APPL.US",
        "symbol": "APPL.US",
        "low": 13.175,
        "close": 13.32,
        "open": 13.39,
        "date": "2022-11-01",
    }

    fake_stock_call = StockCall(fake_stock_data)
    fake_stock_call.user_id = 2

    db.session.add(fake_stock_call)
    db.session.commit()

    response = test_client.get(
        "/api/v1/users/history",
        headers={"Authorization": "Bearer {}".format(user_token)},
    )
    assert len(response.get_json()) == 1
    assert response.status_code == 200

    fake_stock_call = StockCall(fake_stock_data)
    fake_stock_call.user_id = 2

    db.session.add(fake_stock_call)
    db.session.commit()

    response = test_client.get(
        "/api/v1/users/history",
        headers={"Authorization": "Bearer {}".format(user_token)},
    )
    assert len(response.get_json()) == 2
    assert response.status_code == 200


def test_unauthorized_history(test_client):
    response = test_client.get("/api/v1/users/history")
    assert b"Missing Authorization Header" in response.data
    assert response.status_code == 401
