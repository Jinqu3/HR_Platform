from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ApplicantCreate(BaseModel):
    full_name: str = Field(...)
    email: EmailStr = Field(...)
    phone: str | None = Field(default=None)
    password: str = Field(default="default_password")


class ApplicantUpdate(BaseModel):
    full_name: str = Field(...)
    email: EmailStr = Field(...)
    phone: str | None = Field(default=None)
    resume_path: str | None = Field(default=None)
    skills: str | None = Field(default=None)


class ApplicantPatch(BaseModel):
    full_name: str | None = Field(default=None)
    email: EmailStr | None = Field(default=None)
    phone: str | None = Field(default=None)
    resume_path: str | None = Field(default=None)
    skills: str | None = Field(default=None)


class Applicant(BaseModel):
    id: UUID = Field(...)
    full_name: str = Field(...)
    email: EmailStr = Field(...)
    phone: str | None = Field(default=None)
    resume_path: str | None = Field(default=None)
    created_at: datetime = Field(...)

    model_config = ConfigDict(from_attributes=True)
