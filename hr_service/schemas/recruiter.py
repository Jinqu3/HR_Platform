from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RecruiterCreate(BaseModel):
    full_name: str = Field(...)
    email: EmailStr = Field(...)
    company_id: UUID | None = Field(default=None)
    is_active: bool = Field(default=True)
    password: str = Field(default="default_password")


class RecruiterUpdate(BaseModel):
    full_name: str = Field(...)
    email: EmailStr = Field(...)
    company_id: UUID | None = Field(default=None)
    is_active: bool = Field(...)


class RecruiterPatch(BaseModel):
    full_name: str | None = Field(default=None)
    email: EmailStr | None = Field(default=None)
    company_id: UUID | None = Field(default=None)
    is_active: bool | None = Field(default=None)


class Recruiter(BaseModel):
    id: UUID = Field(...)
    full_name: str = Field(...)
    email: EmailStr = Field(...)
    company_id: UUID | None = Field(default=None)
    is_active: bool = Field(...)
    created_at: datetime = Field(...)

    model_config = ConfigDict(from_attributes=True)
