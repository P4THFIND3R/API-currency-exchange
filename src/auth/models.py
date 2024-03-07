from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, String, ForeignKey
from datetime import datetime

from src.backend.db_config import Base
from src.models.models import Users

from src.auth.schemas import Session as SessionSchema


# Перенести в auth
class Sessions(Base):
    __tablename__ = 'sessions'

    session_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, index=True)
    refresh_token: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey(Users.user_id))
    fingerprint: Mapped[str]
    exp_at: Mapped[float]
    created_at: Mapped[datetime]

    @staticmethod
    def get_primary_key() -> int:
        return Sessions.session_id

    def model_dump_to_pydantic(self) -> SessionSchema:
        return SessionSchema(
            session_id=self.session_id,
            refresh_token=self.refresh_token,
            user_id=self.user_id,
            fingerprint=self.fingerprint,
            exp_at=self.exp_at,
            created_at=self.created_at
        )
