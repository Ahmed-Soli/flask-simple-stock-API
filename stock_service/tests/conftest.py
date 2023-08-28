# encoding: utf-8

import pytest
from dotenv import load_dotenv
from stock_service.app import create_app
from stock_service.clients.stooq import StooqClient


@pytest.fixture
def test_client():
    load_dotenv(".testenv")
    app = create_app(testing=True)
    return app.test_client()


@pytest.fixture
def stooq_client():
    return StooqClient("https://example.com/")
