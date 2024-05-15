from tests.conftest import client, HEADERS
from tests.invoice.fixtures import *


def test_base_invoice_data(create_invoice):
    assert create_invoice.get("uuid") == "fixture_invoice_1"
    pass
    headers = HEADERS
    query = f"v1/invoice?is_paid=true"
    response = client.get(
        query,
        headers=headers,
    )

    assert response.status_code == 200
    assert len(response.json().get("result")) == 0

    query = f"v1/invoice?is_paid=false"
    response = client.get(
        query,
        headers=headers,
    )

    assert response.status_code == 200
    assert len(response.json().get("result")) == 1
