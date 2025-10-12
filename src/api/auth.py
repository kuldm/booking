from fastapi import APIRouter, Body
from pwdlib import PasswordHash



from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])

password_hash = PasswordHash.recommended()

@router.post("/register")
async def register_user(
        user_data: UserRequestAdd = Body(openapi_examples={
        "1": {"summary": "Дмитрий", "value": {
            "email": "dmitriy@yandex.ru",
            "password": "123rewggdf",
        }},
        "2": {"summary": "Максим", "value": {
            "email": "maksim@google.com",
            "password": "fdsghsdh34t",
        }},
        }
        ),
):
    hashed_password = password_hash.hash(user_data.password)
    new_user_data = UserAdd(email=user_data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK"}
