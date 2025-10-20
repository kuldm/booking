from sqlalchemy import select, func

from src.database import engine
from src.models.bookings import BookingsModel
from src.models.rooms import RoomsModel
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
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

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from,
            date_to,
    ):
        """
        with rooms_count as (
            SELECT room_id, count(*) as rooms_booked from public.bookings
            where date_to >= '2025-08-01' and date_from <= '2025-10-07'
            group by room_id
        ),
        rooms_left_table as (
            select rooms.id as room_id, quantity - coalesce(rooms_booked, 0)  as rooms_left
            from rooms
            left join rooms_count on rooms.id = rooms_count.room_id
        )
        select * from rooms_left_table
        where rooms_left > 0 and room_id in (select id from rooms where hotel_id = 26);
        """
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        return await self.get_filtered(RoomsModel.id.in_(rooms_ids_to_get))