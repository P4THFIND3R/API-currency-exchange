from typing import Annotated
from fastapi import Depends, Request

from src.auth.schemas import Tokens
from src.services.sessions_service import SessionsService
from src.services.users_service import UsersService
from src.utils.uow import IUnitOfWork, UnitOfWork
from src.auth import security

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]


async def get_sessions_service(uow: UOWDep) -> SessionsService:
    return SessionsService(uow)


async def get_users_service(uow: UOWDep) -> UsersService:
    return UsersService(uow)


users_service_dep = Annotated[UsersService, Depends(get_users_service)]
sessions_service_dep = Annotated[SessionsService, Depends(get_sessions_service)]
fingerprint_dep = Annotated[str, Depends(security.get_fingerprint)]
tokens_dep = Annotated[Tokens, Depends(security.get_tokens)]
