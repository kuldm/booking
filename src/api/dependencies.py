from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1, description="Порядковый номер страницы")]
    per_page: Annotated[int | None, Query(None, ge=1, le=30, description="Cколько записей выводить на каждой странице")]


PaginationDep = Annotated[PaginationParams, Depends()]
