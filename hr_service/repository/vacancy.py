from hr_service.models.vacancy import Vacancy
from hr_service.repository.base import BaseRepository
from schemas.mapper.mappers import VacancyMapper


class VacancyRepository(BaseRepository):
    model = Vacancy
    mapper = VacancyMapper
