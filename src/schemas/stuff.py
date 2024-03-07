from pydantic import BaseModel
from enum import Enum


class Roles(Enum):
    guest = 'guest'
    user = 'user'
    admin = 'admin'
