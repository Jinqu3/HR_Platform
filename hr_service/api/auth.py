from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from hr_service.api.dependencies import DBDep
from hr_service.schemas.applicant import Applicant, ApplicantCreate
from hr_service.schemas.auth import Token, UserLogin
from hr_service.schemas.recruiter import Recruiter, RecruiterCreate
from hr_service.service.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/register/hr", response_model=Recruiter)
async def register_hr(db: DBDep, data: RecruiterCreate = Body()):
    return await AuthService(db).register_hr(data=data)


@router.post("/register/applicant", response_model=Applicant)
async def register_applicant(db: DBDep, data: ApplicantCreate = Body()):
    return await AuthService(db).register_applicant(data=data)


@router.post("/login", response_model=Token)
async def login(db: DBDep, data: UserLogin = Body()):
    return await AuthService(db).login(data=data)


@router.post("/login/hr", response_model=Token)
async def login_hr(db: DBDep, data: UserLogin = Body()):
    data.role = "hr"
    return await AuthService(db).login(data=data)


@router.post("/login/applicant", response_model=Token)
async def login_applicant(db: DBDep, data: UserLogin = Body()):
    data.role = "applicant"
    return await AuthService(db).login(data=data)


async def get_current_user(db: DBDep, token: str = Depends(oauth2_scheme)):
    return await AuthService(db).get_current_user_from_token(token)


async def get_current_hr(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "hr":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized. HR role required.")
    return current_user["user"]


async def get_current_applicant(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "applicant":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized. Applicant role required.")
    return current_user["user"]


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return {"role": current_user["role"], "data": current_user["user"]}
