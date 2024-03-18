from src.auth.schemas import Session, SessionCreate
from src.utils.uow import IUnitOfWork


class SessionsService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_session(self, refresh_token: str) -> Session:
        async with self.uow:
            session: Session = await self.uow.sessions_repos.get_session_by_refresh_token(refresh_token)
            if session:
                return Session.model_validate(session)

    async def add_session(self, session_data: SessionCreate):
        async with self.uow:
            # if there are more than 5 active sessions -> close them all
            user_sessions = await self.get_user_sessions(session_data.user_id)
            if len(user_sessions) >= 5:
                print(f"user {session_data.user_id} sessions have been deleted")
                await self.uow.sessions_repos.clear_user_sessions(session_data.user_id)

            # create new session record
            stmt = await self.uow.sessions_repos.add_one(session_data.model_dump())
            result = Session.model_validate(stmt)

            # committing
            await self.uow.commit()
            print(f"Session {result.session_id} created")
            return result

    async def get_user_sessions(self, user_id) -> list[Session]:
        stmt = await self.uow.sessions_repos.get_sessions_by_user_id(user_id)
        return [Session.model_validate(session) for session in stmt]


