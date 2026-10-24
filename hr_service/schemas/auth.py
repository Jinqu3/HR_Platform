from pydantic import BaseModel, EmailStr, Field


class UserLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)
    role: str | None = Field(default=None, description="'hr' or 'applicant' (optional, auto-detected if omitted)")


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
