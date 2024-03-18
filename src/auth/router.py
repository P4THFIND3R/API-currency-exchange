from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from src.auth.dependencies import users_service_dep, sessions_service_dep, fingerprint_dep, tokens_dep
from src.schemas.user import User
from src.auth import security
from src.auth.schemas import Tokens, Payload
from src.exceptions import TokensSetSuccessfully, AccessTokenExpired

auth_router = APIRouter(prefix='/auth')


async def check_user(userdata: Annotated[OAuth2PasswordRequestForm, Depends()], user_service: users_service_dep):
    user = await user_service.get_user(username=userdata.username)
    return security.authentication(userdata, user)


@auth_router.post('')
async def authentication(response: Response,
                         session_service: sessions_service_dep, fingerprint: fingerprint_dep,
                         user: User = Depends(check_user), ):
    # create access and refresh tokens
    access_token = security.create_access_token(user)
    refresh_token = security.create_session(user, fingerprint)
    # add an entry to the db
    session = await session_service.add_session(refresh_token)

    # setting tokens in cookies
    response.set_cookie('access_token', access_token, httponly=True)
    response.set_cookie('refresh_token', session.refresh_token, httponly=True)

    return {'access_token': access_token}


@auth_router.post('/update')
async def update_tokens(response: Response, tokens: tokens_dep,
                        sessions_service: sessions_service_dep, users_service: users_service_dep,
                        fingerprint: fingerprint_dep):
    # get session by refresh token
    session = await sessions_service.get_session(tokens.refresh_token)
    # check if session is valid and not expired
    user_id = security.check_session(session, fingerprint)

    # getting user
    user = await users_service.get_user(user_id)
    user = security.get_user_view(user)

    # create access and refresh tokens
    access_token = security.create_access_token(user)
    session = await sessions_service.add_session(security.create_session(user, fingerprint))
    refresh_token = session.refresh_token

    # setting tokens in cookies
    response.set_cookie('access_token', access_token, httponly=True)
    response.set_cookie('refresh_token', refresh_token, httponly=True)

    return Tokens(access_token=access_token, refresh_token=refresh_token)


@auth_router.post('/authorize')
async def authorize(response: Response, tokens: tokens_dep,
                    sessions_service: sessions_service_dep, users_service: users_service_dep,
                    fingerprint: fingerprint_dep):
    try:
        payload = await security.check_access_token(tokens.access_token)
    except AccessTokenExpired:
        tokens = await update_tokens(response, tokens, sessions_service, users_service, fingerprint)
        # setting tokens in cookies
        response.set_cookie('access_token', tokens.access_token, httponly=True)
        response.set_cookie('refresh_token', tokens.refresh_token, httponly=True)
        payload = await security.check_access_token(tokens.access_token)
    return Payload.model_validate(payload)


@auth_router.get('/protected')
async def protected(user_payload: Payload = Depends(authorize)):
    return user_payload.role, user_payload.exp
