from abc import ABC, abstractmethod

from src.backend.db_config import async_session_maker
from src.repositories.repositories import SessionRepository, UserRepository


class IUnitOfWork(ABC):
    sessions_repos: SessionRepository
    users_repos: UserRepository

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        # repositories
        self.sessions_repos = SessionRepository(self.session)
        self.users_repos = UserRepository(self.session)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()
        await self.session.close()

    async def rollback(self):
        await self.session.rollback()

    async def commit(self):
        await self.session.commit()
