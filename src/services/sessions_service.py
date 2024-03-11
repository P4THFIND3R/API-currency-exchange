from src.auth.schemas import Session, SessionCreate
from src.utils.uow import IUnitOfWork


class SessionsService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_session(self, session_id: int) -> Session:
        async with self.uow:
            session: Session = await self.uow.sessions_repos.find_by_id(session_id)
            if session:
                return Session.model_validate(session)

    async def create_session(self, session_data: SessionCreate):
        async with self.uow:
            stmt = await self.uow.sessions_repos.add_one(session_data.model_dump())
            result = Session.model_validate(stmt)
            await self.uow.commit()
            return result
