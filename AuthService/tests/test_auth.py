import pytest

# Тест регистрации пользователя
@pytest.mark.asyncio
async def test_register_user(async_client):
    response = await async_client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

# Тест входа пользователя
@pytest.mark.asyncio
async def test_login_user(async_client):
    # Регистрируем пользователя
    await async_client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123"
        },
    )
    # Логинимся
    response = await async_client.post(
        "/auth/login",
        json={
            "username": "testuser",
            "password": "password123"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

# Тест обновления токена
@pytest.mark.asyncio
async def test_refresh_token(async_client):
    # Регистрируем пользователя
    register_response = await async_client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123"
        },
    )
    assert register_response.status_code == 200
    refresh_token = register_response.json()["refresh_token"]

    # Обновляем токен
    response = await async_client.post(
        "/auth/token/refresh",
        json={"refresh_token": refresh_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
