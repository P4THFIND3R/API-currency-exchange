from pydantic import BaseModel
from typing import Annotated


class CurrenciesToExchange(BaseModel):
    amount: Annotated[int | float, 'the amount of money to be exchanged']
    convert_from: str
    convert_to: str
