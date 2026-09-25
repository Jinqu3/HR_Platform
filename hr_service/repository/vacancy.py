from schemas.mapper.mappers import VacancyMapper

from hr_service.models.vacancy import Vacancy
from hr_service.repository.base import BaseRepository


class VacancyRepository(BaseRepository):
    model = Vacancy
    mapper = VacancyMapper
