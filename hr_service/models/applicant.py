from datetime import datetime

from sqlalchemy import String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from hr_service.database import Base


class Applicant(Base):
    __tablename__ = "applicants"

    full_name: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="ФИО соискателя"
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, comment="Email соискателя"
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255), nullable=True, comment="Хэш пароля"
    )
    phone: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="Телефон соискателя"
    )
    resume_path: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="Путь к резюме"
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False, comment="Дата регистрации"
    )
