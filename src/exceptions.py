from fastapi import HTTPException


class UserNotFoundError(HTTPException):
    def __init__(self, detail: str = "User not found!", status_code: int = 404):
        super().__init__(status_code=status_code, detail=detail)


class AuthenticationError(HTTPException):
    def __init__(self, detail: str = "Login or password is not valid", status_code: int = 403):
        super().__init__(status_code=status_code, detail=detail)


class TokenNotFoundError(HTTPException):
    def __init__(self, detail: str = "A valid access and refresh token are required", status_code: int = 403):
        super().__init__(status_code=status_code, detail=detail)


class TokenError(HTTPException):
    def __init__(self, detail: str = "322", status_code: int = 403):
        super().__init__(status_code=status_code, detail=detail)


class RefreshTokenExpired(HTTPException):
    def __init__(self, detail: str = "Refresh token has expired", status_code: int = 403):
        super().__init__(status_code=status_code, detail=detail)


class AccessTokenExpired(HTTPException):
    def __init__(self, detail: str = "Access token has expired", status_code: int = 403):
        super().__init__(status_code=status_code, detail=detail)


class TokensSetSuccessfully(HTTPException):
    def __init__(self, detail: str = "Tokens set successfully!", status_code: int = 200):
        super().__init__(status_code=status_code, detail=detail)
