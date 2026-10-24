from hr_service.models.application import Application
from hr_service.repository.base import BaseRepository
from schemas.mapper.mappers import ApplicationMapper


class ApplicationRepository(BaseRepository):
    model = Application
    mapper = ApplicationMapper
