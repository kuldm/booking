from pydantic import EmailStr
from sqlalchemy import select

from src.models.users import UsersModel
from src.repositories.base import BaseRepository
from src.schemas.users import User, UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersModel
    schema = User

    async def get_user_with_hashed_password(self, email: EmailStr) -> UserWithHashedPassword:
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPassword.model_validate(model)
