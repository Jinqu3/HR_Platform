from hr_service.repository.applicant import ApplicantRepository
from hr_service.repository.application import ApplicationRepository
from hr_service.repository.company import CompanyRepository
from hr_service.repository.recruiter import RecruiterRepository
from hr_service.repository.vacancy import VacancyRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.vacancies = VacancyRepository(self.session)
        self.companies = CompanyRepository(self.session)
        self.applicants = ApplicantRepository(self.session)
        self.applications = ApplicationRepository(self.session)
        self.recruiters = RecruiterRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
