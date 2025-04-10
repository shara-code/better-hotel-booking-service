import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("best@email.com", "ever", 200),
        ("best@email.com", "3ver", 409),
        ("roman@dev.com", "dev", 200),
        ("abcde", "abcde", 422),
        ("slim_shady@email.com", "eminem", 200),
    ],
)
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("test@test.com", "test", 200),
        ("artem@example.com", "artem", 200),
        ("wrong@person.com", "unknown", 401),
    ],
)
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == status_code
