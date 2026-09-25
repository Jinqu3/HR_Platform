from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class VacancyGet(BaseModel):

    title: str = Field(...)
    stack: str = Field(...)
    experience: float = Field(...)
    requirements: str = Field(...)
    salary: float = Field(...)
    created_at: datetime = Field(...)


class VacancyUpdate(BaseModel):
    title: str = Field(...)
    stack: str = Field(...)
    experience: float = Field(...)
    requirements: str = Field(...)
    salary: float = Field(...)


class VacancyPatch(BaseModel):
    title: str | None = Field(default=None)
    stack: str | None = Field(default=None)
    experience: float | None = Field(default=None)
    requirements: str | None = Field(default=None)
    salary: float | None = Field(default=None)


class VacancyCreate(BaseModel):
    title: str = Field(...)
    stack: str = Field(...)
    experience: float = Field(...)
    requirements: str = Field(...)
    salary: float = Field(...)
    is_active: bool = Field(...)
    company_id: UUID = Field(...)


class Vacancy(VacancyGet):
    id: UUID = Field(...)
    company_id: UUID = Field(...)

    model_config = ConfigDict(from_attributes=True)
