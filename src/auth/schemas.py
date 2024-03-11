from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Annotated
from src.schemas.stuff import Roles


class SessionCreate(BaseModel):
    refresh_token: str
    user_id: int
    fingerprint: str
    exp_at: Annotated[float, 'datetime.timestamp()']
    created_at: Annotated[float | datetime, 'datetime.timestamp(), datetime'] = datetime.now()


class Session(SessionCreate):
    session_id: int

    model_config = ConfigDict(from_attributes=True)


class Payload(BaseModel):
    username: str
    role: Roles | str
    exp: float


class Tokens(BaseModel):
    access_token: str
    refresh_token: str
