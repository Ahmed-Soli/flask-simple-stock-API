def test_stock_query_resource_get(test_client, user_token, mocker):
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

    mock_stock_client = mocker.patch(
        "api_service.api.resources.StockQuery.stock_client"
    )
    mock_stock_client.get_stock.return_value = fake_stock_data

    expected_result = {"company_name": "APPL.US", "symbol": "APPL.US", "quote": 13.32}

    response = test_client.get(
        "/api/v1/stock?q=test",
        headers={"Authorization": "Bearer {}".format(user_token)},
    )
    assert response.get_json() == expected_result
    assert response.status_code == 200
    mock_stock_client.get_stock.assert_called_once_with("test")


def test_stock_query_resource_unauthorized_get(test_client, mocker):
    mock_stock_client = mocker.patch(
        "api_service.api.resources.StockQuery.stock_client"
    )

    response = test_client.get("/api/v1/stock?q=test")
    assert b"Missing Authorization Header" in response.data
    assert response.status_code == 401
    mock_stock_client.get_stock.assert_not_called()


def test_stock_query_resource_get_with_unavailable_quote(
    test_client, user_token, mocker
):
    fake_stock_data = {
        "high": None,
        "low": None,
        "open": None,
        "close": None,
        "name": "APPL.US",
        "date": None,
        "time": None,
        "symbol": "APPL.US",
    }

    mock_stock_client = mocker.patch(
        "api_service.api.resources.StockQuery.stock_client"
    )
    mock_stock_client.get_stock.return_value = fake_stock_data

    response = test_client.get(
        "/api/v1/stock?q=test",
        headers={"Authorization": "Bearer {}".format(user_token)},
    )
    assert b"Stock quote not available" in response.data
    assert response.status_code == 404
    mock_stock_client.get_stock.assert_called_once_with("test")


def test_stock_query_resource_invalid_get(test_client, user_token, mocker):
    mock_stock_client = mocker.patch(
        "api_service.api.resources.StockQuery.stock_client"
    )

    response = test_client.get(
        "/api/v1/stock", headers={"Authorization": "Bearer {}".format(user_token)}
    )
    assert b"Missing data for required field" in response.data
    assert response.status_code == 400
    mock_stock_client.get_stock.assert_not_called()


def test_stock_query_resource_get_with_invalid_stock(test_client, user_token, mocker):
    mock_stock_client = mocker.patch(
        "api_service.api.resources.StockQuery.stock_client"
    )
    mock_stock_client.get_stock.return_value = None

    response = test_client.get(
        "/api/v1/stock?q=test",
        headers={"Authorization": "Bearer {}".format(user_token)},
    )
    assert b"Stock not found" in response.data
    assert response.status_code == 404
    mock_stock_client.get_stock.assert_called_once_with("test")
