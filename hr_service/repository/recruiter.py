from schemas.mapper.mappers import RecruiterMapper

from hr_service.models.recruiter import Recruiter
from hr_service.repository.base import BaseRepository


class RecruiterRepository(BaseRepository):
    model = Recruiter
    mapper = RecruiterMapper
