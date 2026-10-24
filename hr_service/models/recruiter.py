from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hr_service.database import Base


class Recruiter(Base):
    __tablename__ = "recruiters"

    full_name: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="ФИО рекрутера"
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, comment="Email рекрутера"
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255), nullable=True, comment="Хэш пароля"
    )
    company_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("companies.id"), nullable=True, comment="ID компании"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False, comment="Активность рекрутера"
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False, comment="Дата создания"
    )

    company_recruiter: Mapped["Company"] = relationship("Company", back_populates="recruiters")  # type: ignore  # noqa: F821
