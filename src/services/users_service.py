from fastapi import HTTPException

from src.schemas.user import UserFromDB, UserRegistration
from src.utils.uow import IUnitOfWork
from src.exceptions import UserNotFoundError


class UsersService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_user(self, user_id: int) -> UserFromDB:
        async with self.uow:
            user: UserFromDB = await self.uow.users_repos.find_by_id(user_id)
            if user:
                return UserFromDB.model_validate(user)
            raise UserNotFoundError

    async def add_user(self, user_data: UserRegistration):
        async with self.uow:
            stmt = await self.uow.users_repos.add_one(user_data.model_dump())
            result = UserFromDB.model_validate(stmt)
            await self.uow.commit()
            return result
