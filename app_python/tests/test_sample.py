import socket
import platform
from fastapi.testclient import TestClient
from infoservice.infoservice import app

client = TestClient(app)

# Test main endpoint
def test_endpoint_main():
    response = client.get("/")
    # Test presence
    assert response.status_code == 200
    # Test verifiable variable fields
    assert response.json()["system"]["hostname"]         == socket.gethostname()
    assert response.json()["system"]["platform"]         == platform.system()
    assert response.json()["system"]["platform_version"] == platform.version()
    assert response.json()["system"]["architecture"]     == platform.machine()
    assert response.json()["system"]["python_version"]   == platform.python_version()


# Test health endpoint
def test_endpoint_health():
    response = client.get("/health")
    # Test presence
    assert response.status_code == 200

# Test request info processing
def test_request_info(mocker):
    """Test how program parses request from different hosts"""
    # First try
    mock_ip = "16.32.64.128"
    mock_client = mocker.patch("fastapi.Request.client")
    mock_client.host = mock_ip
    response = client.get(
            "/",
            headers={
            "user-agent": "noexist",
            }
    )
    assert response.json()["request"]["client_ip"] == mock_ip
    assert response.json()["request"]["user_agent"] == "noexist"

    # Second try
    mock_ip = "8.16.32.64"
    mock_client = mocker.patch("fastapi.Request.client")
    mock_client.host = mock_ip
    response = client.get(
            "/",
            headers={
            "user-agent": "doexist",
            }
    )
    assert response.json()["request"]["client_ip"] == mock_ip
    assert response.json()["request"]["user_agent"] == "doexist"

