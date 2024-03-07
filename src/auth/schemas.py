from pydantic import BaseModel
from datetime import datetime
from typing import Annotated
from src.schemas.stuff import Roles


class Session(BaseModel):
    session_id: int
    refresh_token: str
    user_id: int
    fingerprint: str
    exp_at: Annotated[float, 'datetime.timestamp()']
    created_at: Annotated[float | datetime, 'datetime.timestamp(), datetime']


class Payload(BaseModel):
    username: str
    role: Roles | str
    exp: float


class Tokens(BaseModel):
    access_token: str
    refresh_token: str
