from sqlalchemy import select, func

from src.models.facilities import FacilitiesModels
from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesModels
    schema = Facility

    async def get_all_facilities(
            self,
            title,
            limit,
            offset
    ) -> list[Facility]:
        query = select(FacilitiesModels)
        if title:
            query = query.filter(func.lower(FacilitiesModels.title).contains(title.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
