from httpx import AsyncClient

from tests.errors import OPERATION_FAIL, DATA_CONVERT_FAIL


async def test_get_currency_list(ac: AsyncClient):
    response = await ac.post("/auth/login", data={
        "username": "user_test",
        "password": "password_test"
    })
    my_headers = {'access_token': response.cookies.get('access_token'),
                  'refresh_token': response.cookies.get('refresh_token')}
    response = await ac.get("/currency/list", headers=my_headers)

    assert response.status_code == 200, OPERATION_FAIL


async def test_get_exchange_currency(ac: AsyncClient):
    response = await ac.post("/auth/login", data={
        "username": "user_test",
        "password": "password_test"
    })
    my_headers = {'access_token': response.cookies.get('access_token'),
                  'refresh_token': response.cookies.get('refresh_token')}
    response = await ac.get("/currency/exchange", headers=my_headers)

    assert response.status_code == 200, OPERATION_FAIL
    assert response.text


async def test_exchange_currency(ac: AsyncClient):
    response = await ac.post("/auth/login", data={
        "username": "user_test",
        "password": "password_test"
    })
    my_headers = {'access_token': response.cookies.get('access_token'),
                  'refresh_token': response.cookies.get('refresh_token')}
    response = await ac.post("/currency/exchange", headers=my_headers, json={
        'amount': 10, 'convert_from': 'USD', 'convert_to': 'RUB'})

    assert response.status_code == 200, OPERATION_FAIL
    assert response.text
