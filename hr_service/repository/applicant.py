from schemas.mapper.mappers import ApplicantMapper

from hr_service.models.applicant import Applicant
from hr_service.repository.base import BaseRepository


class ApplicantRepository(BaseRepository):
    model = Applicant
    mapper = ApplicantMapper
