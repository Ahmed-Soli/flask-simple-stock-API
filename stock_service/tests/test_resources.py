from stock_service.clients.stooq import StooqObject


def test_stock_resource_get(test_client, mocker):
    fake_stooq_data = StooqObject(
        {
            "Symbol": "APPL.US",
            "Date": "N/D",
            "Time": "N/D",
            "Open": "N/D",
            "High": "N/D",
            "Low": "N/D",
            "Close": "N/D",
            "Volume": "N/D",
            "Name": "APPL.US",
        }
    )

    mock_stooq_client = mocker.patch(
        "stock_service.api.resources.StockResource.stooq_client"
    )
    mock_stooq_client.get_stock.return_value = fake_stooq_data

    expected_result = {
        "high": None,
        "low": None,
        "open": None,
        "close": None,
        "name": "APPL.US",
        "date": None,
        "time": None,
        "symbol": "APPL.US",
    }

    response = test_client.get("/api/v1/stock?q=test")
    assert response.get_json() == expected_result
    assert response.status_code == 200
    mock_stooq_client.get_stock.assert_called_once_with("test")


def test_stock_resource_invalid_get(test_client, mocker):
    mock_stooq_client = mocker.patch(
        "stock_service.api.resources.StockResource.stooq_client"
    )

    response = test_client.get("/api/v1/stock")
    assert b"Missing data for required field" in response.data
    assert response.status_code == 400
    mock_stooq_client.get_stock.assert_not_called()


def test_stock_resource_get_with_invalid_stock(test_client, mocker):
    mock_stooq_client = mocker.patch(
        "stock_service.api.resources.StockResource.stooq_client"
    )
    mock_stooq_client.get_stock.return_value = None

    response = test_client.get("/api/v1/stock?q=test")
    assert b"Stock not found" in response.data
    assert response.status_code == 404
    mock_stooq_client.get_stock.assert_called_once_with("test")
