from api_service.models import StockCall


def test_stats(test_client, db, admin_token):
    db.session.query(StockCall).delete()
    db.session.commit()

    expected_result = []

    response = test_client.get(
        "/api/v1/stats",
        headers={"Authorization": "Bearer {}".format(admin_token)},
    )
    assert response.get_json() == expected_result
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
    fake_stock_call.user_id = 1

    db.session.add(fake_stock_call)
    db.session.commit()

    expected_result = [
        {"times_requested": 1, "symbol": "APPL.US"},
    ]

    response = test_client.get(
        "/api/v1/stats",
        headers={"Authorization": "Bearer {}".format(admin_token)},
    )
    assert response.get_json() == expected_result
    assert response.status_code == 200

    fake_stock_data["symbol"] = "AU.US"

    fake_stock_call = StockCall(fake_stock_data)
    fake_stock_call.user_id = 1

    db.session.add(fake_stock_call)
    db.session.commit()

    fake_stock_call = StockCall(fake_stock_data)
    fake_stock_call.user_id = 1

    db.session.add(fake_stock_call)
    db.session.commit()

    expected_result = [
        {"times_requested": 2, "symbol": "AU.US"},
        {"times_requested": 1, "symbol": "APPL.US"},
    ]

    response = test_client.get(
        "/api/v1/stats",
        headers={"Authorization": "Bearer {}".format(admin_token)},
    )
    assert response.get_json() == expected_result
    assert response.status_code == 200


def test_unauthorized_stats(test_client):
    response = test_client.get(
        "/api/v1/stats",
    )
    response = test_client.get("/api/v1/stats")
    assert b"Missing Authorization Header" in response.data
    assert response.status_code == 401


def test_unauthorized_user_stats(test_client, user_token):
    response = test_client.get(
        "/api/v1/stats",
        headers={"Authorization": "Bearer {}".format(user_token)},
    )
    assert b"Unauthorized" in response.data
    assert response.status_code == 403
