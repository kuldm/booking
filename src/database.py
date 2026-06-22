from datetime import datetime

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, NullPool
from sqlalchemy.sql import func

from src.config import settings

engine = create_async_engine(settings.DB_URL, echo=True)
# Для celery beat чтобы при подключении к бд не создавался каждый раз новый ивент луп так как для алхимии это не нравится
engine_null_pool = create_async_engine(settings.DB_URL, echo=True, poolclass=NullPool)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
async_session_maker_null_pool = async_sessionmaker(bind=engine_null_pool, expire_on_commit=False)

session = async_session_maker()


# Это специально пустой класс который нужен для того чтобы от него наследовать все модели. И он будет в себе содержать
# все метаданные моделей которые будут передавать в дальнейшем в alembic
class Base(DeclarativeBase):
    pass


# Миксин для добавления временных меток
class TimestampMixin:
    """Добавляет поля created_at и updated_at ко всем моделям"""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Дата создания записи"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        comment="Дата последнего обновления"
    )
