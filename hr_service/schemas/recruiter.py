from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class RecruiterCreate(BaseModel):
    full_name: str = Field(...)
    email: str = Field(...)
    company_id: UUID | None = Field(default=None)
    is_active: bool = Field(default=True)


class RecruiterUpdate(BaseModel):
    full_name: str = Field(...)
    email: str = Field(...)
    company_id: UUID | None = Field(default=None)
    is_active: bool = Field(...)


class RecruiterPatch(BaseModel):
    full_name: str | None = Field(default=None)
    email: str | None = Field(default=None)
    company_id: UUID | None = Field(default=None)
    is_active: bool | None = Field(default=None)


class Recruiter(RecruiterCreate):
    id: UUID = Field(...)
    created_at: datetime = Field(...)

    model_config = ConfigDict(from_attributes=True)
