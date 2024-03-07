from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, String, ForeignKey
from datetime import datetime

from src.backend.db_config import Base
from src.schemas.user import UserFromDB


class Roles(Base):
    __tablename__ = 'roles'

    role: Mapped[str] = mapped_column(String, primary_key=True, nullable=False)


class Users(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, autoincrement=True)
    username: Mapped[str]
    password: Mapped[str]
    role: Mapped[str] = mapped_column(ForeignKey(Roles.role))

    @staticmethod
    def get_primary_key():
        return Users.user_id

    def model_dump_to_pydantic(self):
        return UserFromDB(user_id=self.user_id, username=self.username, password=self.password, role=self.role)

