

from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hr_service.database import Base


class Company(Base):
    __tablename__ = "companies"

    title: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="Название компании"
    )
    description: Mapped[str] = mapped_column(
        Text, nullable=True, comment="Описание компании"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=0, comment="Активность вакансии", nullable=False
    )

    vacancies: Mapped[list["Vacancy"]] = relationship("Vacancy", back_populates="company")  # type: ignore  # noqa: F821
    recruiters: Mapped[list["Recruiter"]] = relationship("Recruiter", back_populates="company") # type: ignore  # noqa: F821