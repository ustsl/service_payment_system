import pytest
from tests.conftest import client, HEADERS


@pytest.fixture(scope="session")
def create_invoice():

    # Create a user with a predefined Telegram ID
    query = client.post(
        "v1/invoice",
        json={
            "uuid": "fixture_invoice_1",
            "user_id": "4589",
            "payment_system_name": "cryptocloud",
            "service_system_name": "imvo",
            "amount": 12,
        },
        headers=HEADERS,
    )

    # assert user_data_create.status_code == 200, "Failed to create user"
    instance = query.json()
    return instance
