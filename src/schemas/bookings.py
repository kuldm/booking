from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class BookingAdd(BaseModel):
    user_id: int
    room_id: int
    date_from: datetime
    date_to: datetime
    price: int


class Booking(BookingAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
