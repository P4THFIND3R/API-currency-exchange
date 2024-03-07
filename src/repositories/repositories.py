from src.models.models import Users
from src.auth.models import Sessions
from src.repositories.base_repository import Repository


class UserRepository(Repository):
    model = Users


class SessionRepository(Repository):
    model = Sessions
