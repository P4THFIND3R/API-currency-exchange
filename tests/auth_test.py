import asyncio

from sqlalchemy import insert, select
from httpx import AsyncClient
import os

from src.models.models import Roles
from tests.errors import OPERATION_FAIL, DATA_CONVERT_FAIL
from conftest import async_session_maker

global access_token, refresh_token
access_token: str | None = None
refresh_token: str | None = None


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
        assert result == role, DATA_CONVERT_FAIL


async def test_registration(ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "username": "user_test",
        "password": "password_test"
    })

    assert response.status_code == 200, OPERATION_FAIL
    assert response.json().get("username") == "user_test", DATA_CONVERT_FAIL


async def test_authentication(ac: AsyncClient):
    response = await ac.post("/auth/login", data={
        "username": "user_test",
        "password": "password_test"
    })

    assert response.status_code == 200, OPERATION_FAIL
    assert response.cookies.get('access_token') == response.json().get('access_token'), \
        "access_token не установлен/ошибка конвертации!"
    assert response.cookies.get('refresh_token'), "refresh_token не установлен!"

    global access_token, refresh_token
    access_token, refresh_token = response.cookies.get('access_token'), response.cookies.get('refresh_token')


async def test_update(ac: AsyncClient):
    global access_token, refresh_token

    response = await ac.post("/auth/update", cookies={'access_token': access_token, 'refresh_token': refresh_token})

    assert response.status_code == 200, OPERATION_FAIL
    assert response.cookies.get('access_token') != access_token, "Выданный access токен совпадает с предыдущим!"
    assert response.cookies.get('refresh_token') != refresh_token, "Выданный refresh токен совпадает с предыдущим!"

    access_token, refresh_token = response.cookies.get('access_token'), response.cookies.get('refresh_token')


async def test_authorization(ac: AsyncClient):
    response = await ac.post("/auth/authorize", cookies={'access_token': access_token, 'refresh_token': refresh_token})

    assert response.status_code == 200, OPERATION_FAIL
    assert response.json()


async def test_autoupdate(ac: AsyncClient):
    """ Тест направлен на проверку работоспособности автоматического обновления access&refresh tokens,
    в случае истечения срока действия JWT токена, или в случае отсутствия access_token в куках.
    """
    global access_token, refresh_token

    ''' Процедура обновления токенов происходит равнозначно в случаях, если access_token истек или отсутствует в cookies
        Если необходимо так-же проверить случай истечения срока жизни токена - раскомментируйте код '''
    # await asyncio.sleep(60)
    # response = await ac.post("/auth/authorize", cookies={'access_token': access_token, 'refresh_token': refresh_token})

    # в случае отсутствия access_token в куках начнется процедура обновления токенов.
    response = await ac.post("/auth/authorize", cookies={'access_token': '', 'refresh_token': refresh_token})

    assert response.status_code == 200, OPERATION_FAIL
    assert response.cookies.get('refresh_token') != refresh_token, "Обновление токенов произведено не было!"