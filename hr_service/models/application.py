from datetime import datetime
from uuid import UUID as uuid

from sqlalchemy import UUID, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hr_service.database import Base


class Application(Base):
    __tablename__ = "applications"

    applicant_id: Mapped[UUID] = mapped_column(ForeignKey("applicants.id"))
    vacancy_id: Mapped[UUID] = mapped_column(ForeignKey("vacancies.id"))

    status: Mapped[str] = mapped_column(String(50), default="new", comment="Статус отклика: 'new', 'interview', 'rejected', 'hired'")
    task_id: Mapped[uuid | None] = mapped_column(UUID(as_uuid=True), comment="ID Celery Task")
    evaluated_text: Mapped[str | None] = mapped_column(Text)
    evaluation_score: Mapped[float| int | None] = mapped_column(Float)
    applied_at: Mapped[datetime] = mapped_column(server_default=func.now())
    
    applicant: Mapped["Applicant"] = relationship("Applicant")  # type: ignore  # noqa: F821
    vacancy: Mapped["Vacancy"] = relationship("Vacancy")  # type: ignore  # noqa: F821
