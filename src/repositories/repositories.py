from sqlalchemy import select, delete

from src.models.models import Users
from src.auth.models import Sessions
from src.repositories.base_repository import Repository


class UserRepository(Repository):
    model = Users

    async def find_by_username(self, username: str) -> model:
        model = self.model
        stmt = await self.session.execute(select(model).where(model.username == username))
        result: model = stmt.scalars().first()
        return result

    async def find_by_id(self, user_id: int) -> model:
        model = self.model
        stmt = await self.session.execute(select(model).where(model.get_primary_key() == user_id))
        result: model = stmt.scalars().first()
        return result


class SessionRepository(Repository):
    model = Sessions

    async def get_sessions_by_user_id(self, user_id: int):
        stmt = await self.session.execute(select(self.model).where(self.model.user_id == user_id))
        return stmt.scalars().all()

    async def clear_user_sessions(self, user_id: int):
        stmt = await self.session.execute(
            delete(self.model).where(self.model.user_id == user_id).returning(self.model.session_id))
        return stmt

    async def get_session_by_refresh_token(self, refresh_token: str):
        stmt = await self.session.execute(select(self.model).where(self.model.refresh_token == refresh_token))
        return stmt.scalars().first()
