from fastapi.testclient import TestClient
from MessangerService.main import app

client = TestClient(app)










def test_create_chat():
    response = client.post(
        "/api/chats",
        json={"name": "Test Group", "is_group": True, "members": [1, 2, 3]},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Group"
    assert data["is_group"] is True
    assert len(data["members"]) == 3

def test_get_chat_members():
    response = client.get("/api/chats/1/members")
    assert response.status_code == 200
    members = response.json()
    assert isinstance(members, list)
    assert 1 in members
