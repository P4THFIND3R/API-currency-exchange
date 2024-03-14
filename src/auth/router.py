import jwt.exceptions
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from src.auth.dependencies import users_service_dep, sessions_service_dep, fingerprint_dep
from src.schemas.user import User
from src.auth import security
from src.auth.schemas import Tokens
from src.exceptions import TokensSetSuccessfully

auth_router = APIRouter(prefix='/auth')


async def check_user(userdata: Annotated[OAuth2PasswordRequestForm, Depends()], user_service: users_service_dep):
    user = await user_service.get_user(username=userdata.username)
    return security.authentication(userdata, user)


@auth_router.post('')
async def authentication(response: Response, request: Request,
                         session_service: sessions_service_dep, fingerprint: fingerprint_dep,
                         user: User = Depends(check_user), ):
    # create access and refresh tokens
    access_token = security.create_access_token(user)
    refresh_token = security.create_refresh_token(user, fingerprint)
    session = await session_service.create_session(refresh_token)

    # setting tokens in cookies
    response.set_cookie('access_token', access_token, httponly=True)
    response.set_cookie('refresh_token', refresh_token.refresh_token, httponly=True)

    # if a redirect was made from the authentication endpoint, we redirect it back
    if request.headers.get('referer') == 'http://127.0.0.1:8080/auth/authorization':
        return RedirectResponse(request.headers.get('referer'), headers=response.headers)

    return TokensSetSuccessfully


@auth_router.post('/update')
async def update_tokens(response: Response, tokens: Annotated[Tokens, Depends(security.get_tokens)],
                        sessions_service: sessions_service_dep, users_service: users_service_dep,
                        fingerprint: fingerprint_dep):
    # get session by refresh token
    session = await sessions_service.get_session(tokens.refresh_token)
    # check if session is valid and not expired
    user_id = security.check_session(session, fingerprint)

    user = await users_service.get_user(user_id)
    user = security.get_user_view(user)

    # create access and refresh tokens
    access_token = security.create_access_token(user)
    refresh_token = await sessions_service.create_session(security.create_refresh_token(user, fingerprint))
    print(refresh_token)

    # setting tokens in cookies
    response.set_cookie('access_token', access_token, httponly=True)
    response.set_cookie('refresh_token', refresh_token.refresh_token, httponly=True)

    return TokensSetSuccessfully


@auth_router.post('/authorization')
async def authorization(tokens: Tokens = Depends(security.get_tokens)):
    if tokens:
        payload = await security.check_jwt(tokens.access_token)
        return payload
    return RedirectResponse('/auth')
