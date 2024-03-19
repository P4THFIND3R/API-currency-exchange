from fastapi import HTTPException


class WrongCurrencyError(HTTPException):
    def __init__(self, detail: str = "You have entered incorrect data for conversion", status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


class WrongAmountError(HTTPException):
    def __init__(self, detail: str = "You have not specified an amount to be converted", status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


class ExternalApiError(HTTPException):
    def __init__(self, detail: str = "You have not specified an amount to be converted", status_code: int = 500):
        super().__init__(status_code=status_code, detail=detail)
