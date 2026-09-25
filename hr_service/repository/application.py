from schemas.mapper.mappers import ApplicationMapper

from hr_service.models.application import Application
from hr_service.repository.base import BaseRepository


class ApplicationRepository(BaseRepository):
    model = Application
    mapper = ApplicationMapper
