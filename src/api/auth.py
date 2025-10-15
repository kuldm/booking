from fastapi import APIRouter, Body, HTTPException, Response

from src.api.dependencies import UserIdDep
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])


@router.post("/register")
async def register_user(
        user_data: UserRequestAdd = Body(openapi_examples={
            "1": {"summary": "Дмитрий", "value": {
                "email": "dmitriy@yandex.ru",
                "password": "111",
            }},
            "2": {"summary": "Максим", "value": {
                "email": "maksim@google.com",
                "password": "111",
            }},
        }),
):
    hashed_password = AuthService().hash_password(user_data.password)
    new_user_data = UserAdd(email=user_data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK"}


@router.post("/login")
async def register_user(
        response: Response,
        user_data: UserRequestAdd = Body(openapi_examples={
            "1": {"summary": "Дмитрий", "value": {
                "email": "dmitriy@yandex.ru",
                "password": "111",
            }},
            "2": {"summary": "Максим", "value": {
                "email": "maksim@google.com",
                "password": "111",
            }},
        }),
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=user_data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
        if not AuthService().verify_password(user_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль не верный")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.get("/me")
async def get_me(
        user_id: UserIdDep,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user


@router.post("/logout")
async def logout_user(
        response: Response,
):
    response.delete_cookie("access_token")
    return {"status": "OK"}