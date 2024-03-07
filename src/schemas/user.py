from pydantic import BaseModel
from src.schemas.stuff import Roles


class UserFromDB(BaseModel):
    user_id: int
    password: str
    username: str
    role: Roles = Roles.guest


class UserLogin(BaseModel):
    username: str
    password: str


class UserAdd(UserLogin):
    role: Roles = Roles.guest
