from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ApplicationCreate(BaseModel):
    applicant_id: UUID = Field(...)
    vacancy_id: UUID = Field(...)


class ApplicationPatch(BaseModel):
    evaluated_text: str | None = Field(default=None)
    evaluation_score: float | None = Field(default=None)
    task_id: UUID | None = Field(default=None)
    status: str | None = Field(default=None)


class Application(ApplicationCreate):
    id: UUID = Field(...)
    applied_at: datetime = Field(...)
    evaluated_text: str | None = Field(...)
    evaluation_score: float | None = Field(...)
    status: str | None = Field(...)

    model_config = ConfigDict(from_attributes=True)
