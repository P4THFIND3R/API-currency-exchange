from sqlalchemy import insert, select
from httpx import AsyncClient

from src.models.models import Roles
from conftest import client, async_session_maker


async def test_add_role():
    async with async_session_maker() as session:
        role = "guest"
        stmt = insert(Roles).values(role=role)
        await session.execute(stmt)
        await session.commit()

        query = select(Roles)
        result = await session.execute(query)
        result = result.scalars().first().role

        assert result, "Роль не добавилась!"
        assert result == role, "Конвертация данных не прошла успешно!"


async def test_registration(ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "username": "user_test",
        "password": "password_test"
    })

    assert response.status_code == 200, "Операция не прошла успешно!"
    assert response.json().get("username") == "user_test", "Конвертация данных не прошла успешно!"


