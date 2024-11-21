from fastapi.testclient import TestClient
from MessengerService.main import app

client = TestClient(app)

def test_send_message():
    response = client.post(
        "/api/messages",
        json={"sender_id": 1, "chat_id": 1, "text": "Hello, World!"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["sender_id"] == 1
    assert data["chat_id"] == 1
    assert data["text"] == "Hello, World!"
