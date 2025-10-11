from sqlalchemy import select, func, insert

from src.models.hotels import HotelsModel
from src.repositories.base import BaseRepository
from src.schemas.hotels import HotelSchema


class HotelsRepository(BaseRepository):
    model = HotelsModel

    async def get_all(
            self,
            location,
            title,
            limit,
            offset,
    ):
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
        return result.scalars().all()

    async def add(self, hotel_data):
        add_hotel_stmt = insert(HotelsModel).values(**hotel_data.model_dump())
        await self.session.execute(add_hotel_stmt)
        return HotelSchema.model_validate(hotel_data)

