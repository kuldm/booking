from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.config import settings



engine = create_async_engine(settings.DB_URL, echo=True)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

session = async_session_maker()

# Это специально пустой класс который нужен для того чтобы от него наследовать все модели. И он будет в себе содержать
# все метаданные моделей которые будут передавать в дальнейшем в alembic
class Base(DeclarativeBase):
    pass
