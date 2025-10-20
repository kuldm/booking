from datetime import date

from sqlalchemy import select, func

from src.models.hotels import HotelsModel
from src.models.rooms import RoomsModel
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsModel
    schema = Hotel


    async def get_all(
            self,
            location,
            title,
            limit,
            offset,
    ) -> list[Hotel]:
        query = select(HotelsModel)
        if location:
            query = query.filter(func.lower(HotelsModel.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsModel.title).contains(title.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in  result.scalars().all()]

    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsModel.hotel_id)
            .select_from(RoomsModel)
            .filter(RoomsModel.id.in_(rooms_ids_to_get))
        )
        return await self.get_filtered(HotelsModel.id.in_(hotels_ids_to_get))


