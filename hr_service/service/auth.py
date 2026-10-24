from fastapi import HTTPException, status

from hr_service.schemas.applicant import ApplicantCreate
from hr_service.schemas.auth import Token, UserLogin
from hr_service.schemas.mapper.mappers import ApplicantMapper, RecruiterMapper
from hr_service.schemas.recruiter import RecruiterCreate
from hr_service.service.base import BaseService
from hr_service.utils.auth_utils import (
    create_access_token,
    decode_access_token,
    verify_password,
)


class AuthService(BaseService):

    async def register_hr(self, data: RecruiterCreate):
        existing = await self.db.recruiters.get_model_by_email(data.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        recruiter = await self.db.recruiters.add(data)
        await self.db.commit()
        return recruiter

    async def register_applicant(self, data: ApplicantCreate):
        existing = await self.db.applicants.get_model_by_email(data.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        applicant = await self.db.applicants.add(data)
        await self.db.commit()
        return applicant

    async def login(self, data: UserLogin):
        role = data.role.lower() if data.role else None

        if role == "hr":
            user = await self.db.recruiters.get_model_by_email(data.email)
            if not user or not verify_password(data.password, getattr(user, "hashed_password", None)):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
            token = create_access_token({"sub": str(user.email), "role": "hr", "id": str(user.id)})
            return Token(access_token=token, token_type="bearer", role="hr")

        elif role == "applicant":
            user = await self.db.applicants.get_model_by_email(data.email)
            if not user or not verify_password(data.password, getattr(user, "hashed_password", None)):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
            token = create_access_token({"sub": str(user.email), "role": "applicant", "id": str(user.id)})
            return Token(access_token=token, token_type="bearer", role="applicant")

        elif role is None:
            # Auto-detect role
            user = await self.db.recruiters.get_model_by_email(data.email)
            if user and verify_password(data.password, getattr(user, "hashed_password", None)):
                token = create_access_token({"sub": str(user.email), "role": "hr", "id": str(user.id)})
                return Token(access_token=token, token_type="bearer", role="hr")

            user = await self.db.applicants.get_model_by_email(data.email)
            if user and verify_password(data.password, getattr(user, "hashed_password", None)):
                token = create_access_token({"sub": str(user.email), "role": "applicant", "id": str(user.id)})
                return Token(access_token=token, token_type="bearer", role="applicant")

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

        else:
            raise HTTPException(status_code=400, detail="Invalid role. Must be 'hr' or 'applicant'")

    async def get_current_user_from_token(self, token: str):
        payload = decode_access_token(token)
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        
        email = payload.get("sub")
        role = payload.get("role")
        
        if not email or not role:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

        if role == "hr":
            user = await self.db.recruiters.get_model_by_email(email)
            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
            return {"user": RecruiterMapper.map_to_domain_entity(user), "role": "hr"}

        elif role == "applicant":
            user = await self.db.applicants.get_model_by_email(email)
            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
            return {"user": ApplicantMapper.map_to_domain_entity(user), "role": "applicant"}

        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid role in token")
