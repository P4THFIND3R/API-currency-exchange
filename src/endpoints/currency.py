from fastapi import APIRouter, Depends

from src.auth.router import authorize
from src.utils.external_api import get_currency_list, currencies_exchange, get_live_list
from src.schemas.user import Payload
from src.schemas.currency import CurrenciesToExchange

router = APIRouter(prefix='/currency', tags=['currency'])


@router.get('/list')
async def get_currency(user: Payload = Depends(authorize)):
    return await get_currency_list()


@router.get('/exchange')
async def exchange_currency(user: Payload = Depends(authorize)):
    return await get_live_list()


@router.post('/exchange')
async def exchange_currency(currencies_to_exchange: CurrenciesToExchange, user: Payload = Depends(authorize)):
    return await currencies_exchange(currencies_to_exchange)
