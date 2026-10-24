from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hr_service.database import Base


class Vacancy(Base):
    __tablename__ = "vacancies"

    title: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="Название вакансии"
    )
    stack: Mapped[str] = mapped_column(Text, nullable=False, comment="Требуемый стек")
    experience: Mapped[float] = mapped_column(
        Float,
        default=0,
        nullable=False,
        comment="Требуемый опыт. Формат: 2.5 = 2 года 6 месяцев",
    )
    requirements: Mapped[str] = mapped_column(
        Text, nullable=False, comment="Требования к вакансии"
    )
    salary: Mapped[int | None] = mapped_column(
        Float, nullable=True, comment="Заработная плата"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=0, comment="Активность вакансии", nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False, comment="Дата создания вакансии"
    )
    company_id: Mapped[UUID] = mapped_column(ForeignKey("companies.id"), nullable=False)

    company_vacancy: Mapped["Company"] = relationship("Company", back_populates="vacancies")  # type: ignore  # noqa: F821
