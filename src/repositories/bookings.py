from datetime import date

from sqlalchemy import select

from src.models.bookings import BookingsModel
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = BookingsModel
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = (select
                 (self.model)
                 .filter(self.model.date_from == date.today())
                 )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in result.scalars().all()]