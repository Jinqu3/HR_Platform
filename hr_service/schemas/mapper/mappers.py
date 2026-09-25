from schemas.mapper.base import DataMapper

from hr_service.models.applicant import Applicant as ApplicantModel
from hr_service.models.application import Application as ApplicationModel
from hr_service.models.company import Company as CompanyModel
from hr_service.models.recruiter import Recruiter as RecruiterModel
from hr_service.models.vacancy import Vacancy as VacancyModel
from hr_service.schemas.applicant import Applicant
from hr_service.schemas.application import Application as ApplicationSchema
from hr_service.schemas.company import Company
from hr_service.schemas.recruiter import Recruiter
from hr_service.schemas.vacancy import Vacancy


class VacancyMapper(DataMapper):
    schema = Vacancy
    db_model = VacancyModel


class CompanyMapper(DataMapper):
    schema = Company
    db_model = CompanyModel


class ApplicantMapper(DataMapper):
    schema = Applicant
    db_model = ApplicantModel


class ApplicationMapper(DataMapper):
    schema = ApplicationSchema
    db_model = ApplicationModel


class RecruiterMapper(DataMapper):
    schema = Recruiter
    db_model = RecruiterModel
