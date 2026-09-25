from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ApplicationCreate(BaseModel):
    applicant_id: UUID = Field(...)
    vacancy_id: UUID = Field(...)
    status: str = Field(default="new")


class ApplicationUpdate(BaseModel):
    status: str = Field(...)


class ApplicationPatch(BaseModel):
    status: str | None = Field(default=None)


class Application(ApplicationCreate):
    id: UUID = Field(...)
    applied_at: datetime = Field(...)

    model_config = ConfigDict(from_attributes=True)
