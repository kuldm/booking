from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        """Извлекает все записи, соответствующие фильтру."""
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by))
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        """Извлекает все записи без фильтра"""
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        """Извлекает одну запись, соответствующую фильтру, или возвращает None."""
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model)

    async def add(self, data: BaseModel):
        """Добавляет новую запись и возвращает созданную запись."""
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return [self.schema.model_validate(model, from_attributes=True)]

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset)).returning(self.model)
        )
        result = await self.session.execute(update_stmt)
        model = result.scalars().one()
        return [self.schema.model_validate(model, from_attributes=True)]

    async def delete(self, **filter_by):
        """Удаляет записи, соответствующие фильтру."""
        delete_stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        await self.session.execute(delete_stmt)
