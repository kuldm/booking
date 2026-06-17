from pydantic import BaseModel, ConfigDict


class FacilityAdd(BaseModel):
    title: str


class Facility(FacilityAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class FacilityPATCH(BaseModel):
    title: str | None = None

    model_config = ConfigDict(from_attributes=True)