from datetime import datetime

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hr_service.database import Base


class Application(Base):
    __tablename__ = "applications"

    applicant_id: Mapped[int] = mapped_column(ForeignKey("applicants.id"))
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancies.id"))

    status: Mapped[str] = mapped_column(String(50), default="new", comment="Статус отклика: 'new', 'interview', 'rejected', 'hired'")

    applied_at: Mapped[datetime] = mapped_column(server_default=func.now())

    applicant: Mapped["Applicant"] = relationship("Applicant")  # type: ignore  # noqa: F821
    vacancy: Mapped["Vacancy"] = relationship("Vacancy")  # type: ignore  # noqa: F821
