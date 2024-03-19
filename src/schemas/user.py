from pydantic import BaseModel, ConfigDict
from src.schemas.stuff import Roles


class UserLogin(BaseModel):
    username: str
    password: str


class UserRegistration(UserLogin):
    role: Roles = Roles.guest.value


class UserFromDB(UserLogin):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    role: Roles


class User(BaseModel):
    user_id: int
    username: str
    role: Roles


class UserAdd(UserLogin):
    role: Roles = Roles.guest


class Payload(BaseModel):
    username: str
    role: Roles | str
    exp: float

    model_config = ConfigDict(from_attributes=True)
