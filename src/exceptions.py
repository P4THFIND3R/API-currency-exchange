from fastapi import HTTPException


class UserNotFoundError(HTTPException):
    def __init__(self, detail: str = "User not found!", status_code: int = 404):
        super().__init__(status_code=status_code, detail=detail)
