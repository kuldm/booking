from sqlalchemy import select, func, insert, delete

from src.models.facilities import FacilitiesModels, RoomsFacilitiesModels
from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility, RoomFacility, RoomFacilityAdd


class FacilitiesRepository(BaseRepository):
    model = FacilitiesModels
    schema = Facility

    async def get_all_facilities(
            self,
            title,
            limit,
            offset
    ) -> list[Facility]:
        """Извлекает все удобства согласно фильтру."""
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


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesModels
    schema = RoomFacility

    async def set_room_facilities(
            self,
            room_id: int,
            facilities_ids: list[int],
    ) -> None:
        """Добавляет удобства для комнат в таблицу m2m которые нужно добавить, а так же удаляет которые нужно удалить."""
        get_current_facilities_ids_query = (
            select(self.model.facility_id)
            .filter_by(room_id=room_id)
        )

        result = await self.session.execute(get_current_facilities_ids_query)
        current_facilities_ids: list[int] = result.scalars().all()
        ids_to_delete: list[int] = list(set(current_facilities_ids) - set(facilities_ids))
        ids_to_insert: list[int] = list(set(facilities_ids) - set(current_facilities_ids))

        if ids_to_delete:
            delete_m2m_facilities_stmt = (
                delete(self.model)
                .filter(
                    self.model.room_id == room_id,
                    self.model.facility_id.in_(ids_to_delete),
                )
            )
            await self.session.execute(delete_m2m_facilities_stmt)

        if ids_to_insert:
            insert_m2m_facilities_stmt = (
                insert(self.model)
                .values([{"room_id": room_id, "facility_id": f_id} for f_id in ids_to_insert])
            )
            await self.session.execute(insert_m2m_facilities_stmt)

    async def get_room_facilities(
            self,
            room_id,
    ) -> list[RoomFacilityAdd]:
        """Извлекает все удобства комнаты по её id."""
        query = select(RoomsFacilitiesModels).where(self.model.room_id == room_id)
        result = await self.session.execute(query)
        result2 = [RoomFacilityAdd.model_validate(model, from_attributes=True) for model in result.scalars().all()]
        return result2
