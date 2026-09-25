from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CompanyCreate(BaseModel):
    title: str = Field(...)
    description: str | None = Field(default=None)
    is_active: bool = Field(default=True)


class CompanyUpdate(BaseModel):
    title: str = Field(...)
    description: str | None = Field(default=None)
    is_active: bool = Field(...)


class CompanyPatch(BaseModel):
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    is_active: bool | None = Field(default=None)


class Company(CompanyCreate):
    id: UUID = Field(...)

    model_config = ConfigDict(from_attributes=True)
