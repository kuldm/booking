from src.schemas.facilities import FacilityAdd


async def test_add_facility_cruds(db):
    facility_data = FacilityAdd(
        title="Биде"
    )
    new_facility = await db.facilities.add(facility_data)

    facility = await db.facilities.get_one_or_none(id=new_facility.id)
    assert facility
    assert facility.id == new_facility.id

    update_facility_data = FacilityAdd(
        title="Гигиенический душ"
    )
    await db.facilities.edit(update_facility_data, id=new_facility.id)
    updated_facility = await db.facilities.get_one_or_none(id=new_facility.id)
    assert updated_facility
    assert updated_facility.id == new_facility.id
    assert updated_facility.title == "Гигиенический душ"

    await db.facilities.delete(id=new_facility.id)

    facility = await db.facilities.get_one_or_none(id=new_facility.id)
    assert not facility
