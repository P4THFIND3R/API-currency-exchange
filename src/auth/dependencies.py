from typing import Annotated
from fastapi import Depends

from src.utils.uow import IUnitOfWork, UnitOfWork

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
