from secrets import token_hex
import jwt
from datetime import datetime, timedelta
from fastapi import Request, Response, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from src.config import settings
from src.schemas.user import UserFromDB, User
from src.exceptions import AuthenticationError, TokenNotFoundError, RefreshTokenExpired, TokenError, AccessTokenExpired
from src.auth.schemas import Session, SessionCreate, Tokens, Payload


def get_user_view(user: UserFromDB):
    return User(username=user.username, user_id=user.user_id, role=user.role)


def authentication(userdata: Annotated[OAuth2PasswordRequestForm, 'user login data'], user: UserFromDB) -> User:
    if user.password == userdata.password:
        return get_user_view(user)
    raise AuthenticationError


def get_fingerprint(request: Request):
    fingerprint = request.headers.get('user-agent')
    return str(fingerprint)


def get_tokens(request: Request):
    access_token = request.cookies.get('access_token')
    refresh_token = request.cookies.get('refresh_token')
    if refresh_token:
        return Tokens(access_token=access_token, refresh_token=refresh_token)
    else:
        raise TokenNotFoundError


def create_access_token(user: User):
    exp = (datetime.now() + timedelta(minutes=settings.access_exp)).timestamp() - 55
    encode_data = {
        'username': user.username,
        'role': user.role.value,
        'exp': exp
    }
    encoded_jwt = jwt.encode(encode_data, key=settings.secret, algorithm=settings.algorithm)
    return encoded_jwt


def create_session(user: User, fingerprint: str):
    create_date = datetime.now()
    refresh_token = token_hex(8)

    session = SessionCreate(
        refresh_token=refresh_token,
        fingerprint=fingerprint,
        user_id=user.user_id,
        exp_at=create_date.timestamp() + settings.refresh_exp,
        created_at=create_date
    )
    return session


async def check_access_token(access_token):
    if not access_token:
        raise AccessTokenExpired
    try:
        payload = jwt.decode(access_token, key=settings.secret, algorithms=[settings.algorithm])
        return Payload.model_validate(payload)
    except jwt.exceptions.DecodeError:
        raise TokenError
    except jwt.exceptions.ExpiredSignatureError:
        raise AccessTokenExpired


def check_session(session: Session, fingerprint: str):
    # check if session exists
    if not session:
        raise TokenError
    # check if session is expired
    if session.exp_at >= (session.created_at + timedelta(days=settings.refresh_exp)).timestamp():
        raise RefreshTokenExpired
    # check if fingerprint is valid
    if session.fingerprint != fingerprint:
        raise TokenError

    return session.user_id


def set_tokens_to_cookies(response: Response, tokens: Tokens):
    response.set_cookie('access_token', tokens.access_token, httponly=True)
    response.set_cookie('refresh_token', tokens.refresh_token, httponly=True)
    return response
