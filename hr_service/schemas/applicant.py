from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ApplicantCreate(BaseModel):
    full_name: str = Field(...)
    email: str = Field(...)
    phone: str | None = Field(default=None)
    resume_text: str | None = Field(default=None)
    resume_path: str | None = Field(default=None)
    skills: str | None = Field(default=None)


class ApplicantUpdate(BaseModel):
    full_name: str = Field(...)
    email: str = Field(...)
    phone: str | None = Field(default=None)
    resume_text: str | None = Field(default=None)
    resume_path: str | None = Field(default=None)
    skills: str | None = Field(default=None)


class ApplicantPatch(BaseModel):
    full_name: str | None = Field(default=None)
    email: str | None = Field(default=None)
    phone: str | None = Field(default=None)
    resume_text: str | None = Field(default=None)
    resume_path: str | None = Field(default=None)
    skills: str | None = Field(default=None)


class Applicant(ApplicantCreate):
    id: UUID = Field(...)
    created_at: datetime = Field(...)

    model_config = ConfigDict(from_attributes=True)
