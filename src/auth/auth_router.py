from fastapi import APIRouter, Depends
from typing import Annotated

from src.services.sessions_service import SessionsService
from src.services.users_service import UsersService
from src.auth.dependencies import UOWDep
from src.schemas.user import UserRegistration

auth_router = APIRouter(prefix='/auth')


async def get_sessions_service(uow: UOWDep) -> SessionsService:
    return SessionsService(uow)


async def get_users_service(uow: UOWDep) -> UsersService:
    return UsersService(uow)


@auth_router.get('/users/{user_id}')
async def get_user(user_id: int, service: UsersService = Depends(get_users_service)):
    result = await service.get_user(user_id)
    return result


@auth_router.post('/users')
async def create_user(userdata: UserRegistration, service: UsersService = Depends(get_users_service)):
    stmt = await service.add_user(userdata)
    return stmt
