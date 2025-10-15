from sqlalchemy import select, func

from src.models.rooms import RoomsModel
from src.repositories.base import BaseRepository
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsModel
    schema = Room

    async def get_all_rooms(
            self,
            title,
            limit,
            offset,
    ) -> list[Room]:
        query = select(RoomsModel)
        if title:
            query = query.filter(func.lower(RoomsModel.title).contains(title.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    async def get_all_hotel_rooms(
            self,
            hotel_id,
            title,
            limit,
            offset,
    ) -> list[Room]:
        query = select(RoomsModel).where(RoomsModel.hotel_id == hotel_id)
        if title:
            query = query.filter(func.lower(RoomsModel.title).contains(title.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
