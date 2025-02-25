import json
import pytest
import jwt
import base64
from datetime import datetime, timedelta, timezone

from app import create_app
from app.app_config.config_secrets import hmac_secret

# Configure HMAC Secret (Same as used in `cfgservice`)
HMAC_SECRET = hmac_secret

@pytest.fixture
def client():
    """Create a test client for Flask"""
    app = create_app()  # ✅ Call the factory function
    app.config["TESTING"] = True
    return app.test_client()

def create_valid_jwt():
    """Generate a valid JWT for testing"""
    payload = {
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
        "credentials": [
            {
                "credential_configuration_id": "test_credential_1",
                "data": {"name": "John Doe"}
            }
        ]
    }
    return jwt.encode(payload, HMAC_SECRET, algorithm="HS256")

def create_expired_jwt():
    """Generate an expired JWT"""
    payload = {
        "exp": datetime.now(timezone.utc) - timedelta(minutes=5),
        "credentials": [
            {
                "credential_configuration_id": "test_credential_1",
                "data": {"name": "John Doe"}
            }
        ]
    }
    return jwt.encode(payload, HMAC_SECRET, algorithm="HS256")

def create_invalid_jwt():
    """Generate a JWT with an invalid signature"""
    payload = {
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
        "credentials": [
            {
                "credential_configuration_id": "test_credential_1",
                "data": {"name": "John Doe"}
            }
        ]
    }
    return jwt.encode(payload, "wrong_secret", algorithm="HS256")

def test_valid_request(client, mocker):
    """Test a valid JWT request"""
    mocker.patch("app.preauthorization.generate_preauth_token", return_value="mocked_pre_auth_code")
    mocker.patch("app.preauthorization.generate_unique_id", return_value="mocked_transaction_id")

    jwt_token = create_valid_jwt()
    response = client.post(
        "/generateCredentialOffer",
        data={"request": jwt_token}
    )

    assert response.status_code == 200
    response_data = response.get_json()
    assert "credential_offer" in response_data
    assert "uri" in response_data
    assert "qr_code" in response_data
    assert "tx_code" in response_data
    assert "transaction_id" in response_data
    assert response_data["transaction_id"] == "mocked_transaction_id"

def test_valid_request_with_transaction_id(client, mocker):
    """Test a valid JWT request with a given transaction_id"""
    mocker.patch("app.preauthorization.generate_preauth_token", return_value="mocked_pre_auth_code")

    jwt_token = create_valid_jwt()
    response = client.post(
        "/generateCredentialOffer?transaction_id=test_tx_id",
        data={"request": jwt_token}
    )

    assert response.status_code == 200
    response_data = response.get_json()
    assert "transaction_id" in response_data
    assert response_data["transaction_id"] == "test_tx_id"

def test_missing_jwt(client):
    """Test missing JWT"""
    response = client.post("/generateCredentialOffer", data={})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Missing JWT request"}

def test_invalid_jwt(client):
    """Test invalid JWT (wrong signature)"""
    jwt_token = create_invalid_jwt()
    response = client.post(
        "/generateCredentialOffer",
        data={"request": jwt_token}
    )

    if HMAC_SECRET:
        assert response.status_code == 400
        assert response.get_json() == {"error": "Invalid JWT"}
    else:
        assert response.status_code == 200

def test_expired_jwt(client):
    """Test expired JWT"""
    jwt_token = create_expired_jwt()
    response = client.post(
        "/generateCredentialOffer",
        data={"request": jwt_token}
    )

    if HMAC_SECRET:
        assert response.status_code == 401
        assert response.get_json() == {"error": "JWT has expired"}
    else:
        assert response.status_code == 200