import aiohttp
from aiocache import cached
from aiocache.serializers import PickleSerializer

from src.schemas.currency import CurrenciesToExchange
from src.config import settings
from src.utils.exceptions import WrongCurrencyError, WrongAmountError, ExternalApiError

my_headers = {'apikey': settings.CURRENCY_DATA_API_KEY}


def check_data(func):
    async def wrapper(*args, **kwargs):
        data = await func(*args, **kwargs)
        if not data.get('success'):
            error_info = data.get('error').get('info')
            status_code = data.get('error').get('code')
            match error_info:
                case "You have entered an invalid \"from\" property. [Example: from=EUR]":
                    raise WrongCurrencyError(detail=error_info, status_code=status_code)
                case "You have not specified an amount to be converted. [Example: amount=5]":
                    raise WrongAmountError(detail=error_info, status_code=status_code)
            raise ExternalApiError(detail=error_info, status_code=status_code)
        return data

    return wrapper


async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=my_headers) as response:
            data = await response.json()
            return data


@cached(ttl=600, serializer=PickleSerializer())
async def get_currency_list() -> dict:
    url = 'https://api.apilayer.com/currency_data/list'
    return await fetch_data(url)


@cached(ttl=30, serializer=PickleSerializer())
async def get_live_list() -> dict:
    url = 'https://api.apilayer.com/currency_data/live'
    return await fetch_data(url)


@check_data
async def currencies_exchange(data: CurrenciesToExchange) -> dict:
    url = f'https://api.apilayer.com/currency_data/convert?to={data.convert_to}&from={data.convert_from}&amount={data.amount}'
    return await fetch_data(url)
