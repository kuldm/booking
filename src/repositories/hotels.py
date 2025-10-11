from src.models.hotels import HotelsModel
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsModel