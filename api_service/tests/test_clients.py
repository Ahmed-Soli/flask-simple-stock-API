import json

import requests
import responses


@responses.activate
def test_get_stock(stock_client):
    fake_code = "appl.us"
    fake_response = json.dumps(
        {
            "high": None,
            "low": None,
            "open": None,
            "close": None,
            "name": "APPL.US",
            "date": None,
            "time": None,
            "symbol": "APPL.US",
        }
    )
    expected_url = "{}{}".format(stock_client.base_url, stock_client.resource_path)

    responses.add(
        responses.GET, expected_url, body=fake_response, status=requests.codes.ok
    )

    expected_data = {
        "high": None,
        "low": None,
        "open": None,
        "close": None,
        "name": "APPL.US",
        "date": None,
        "time": None,
        "symbol": "APPL.US",
    }
    result = stock_client.get_stock(fake_code)
    assert result == expected_data


@responses.activate
def test_get_stock_with_broken_data(stock_client):
    fake_code = "appl.us"
    fake_response = "broken_data"
    expected_url = "{}{}".format(stock_client.base_url, stock_client.resource_path)

    responses.add(
        responses.GET, expected_url, body=fake_response, status=requests.codes.ok
    )

    result = stock_client.get_stock(fake_code)
    assert result is None


@responses.activate
def test_get_stock_with_error(stock_client):
    fake_code = "appl.us"
    fake_response = json.dumps(
        {
            "high": None,
            "low": None,
            "open": None,
            "close": None,
            "name": "APPL.US",
            "date": None,
            "time": None,
            "symbol": "APPL.US",
        }
    )
    expected_url = "{}{}".format(stock_client.base_url, stock_client.resource_path)

    responses.add(
        responses.GET,
        expected_url,
        body=fake_response,
        status=requests.codes.bad_request,
    )

    result = stock_client.get_stock(fake_code)
    assert result is None
