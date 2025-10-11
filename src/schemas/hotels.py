from pydantic import BaseModel, Field


class HotelSchema(BaseModel):
    title: str
    location: str


class HotelPATCHSchema(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)