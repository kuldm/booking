from fastapi import HTTPException, status

from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        """Извлекает все записи, соответствующие фильтру."""
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        """Извлекает одну запись, соответствующую фильтру, или возвращает None."""
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        """Добавляет новую запись и возвращает созданную запись."""
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        return result.scalars().one()

    async def edit(self, data: BaseModel, **filter_by):
        query = update(self.model).filter_by(**filter_by).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(query)
        hotel =  result.scalars().one_or_none()
        if not hotel:
            raise HTTPException(status_code=404, detail=f"Отель с ID {filter_by['id']} не существует")
        return hotel


    async def delete(self, **filter_by):
        """Удаляет записи, соответствующие фильтру."""
        query = delete(self.model).filter_by(**filter_by).returning(self.model)
        result = await self.session.execute(query)
        deleted_count = result.scalars().all()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"Отель с ID {filter_by['id']} не существует")


