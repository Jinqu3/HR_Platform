from schemas.mapper.mappers import CompanyMapper

from hr_service.models.company import Company
from hr_service.repository.base import BaseRepository


class CompanyRepository(BaseRepository):
    model = Company
    mapper = CompanyMapper
