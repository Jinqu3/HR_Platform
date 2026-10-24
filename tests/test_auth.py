import pytest
from httpx import AsyncClient
from hr_service.main import app


@pytest.mark.asyncio
async def test_auth_registration_and_login(async_client: AsyncClient):
    # 1. Register HR
    hr_data = {
        "full_name": "John HR",
        "email": "john.hr@company.com",
        "password": "secretpassword",
        "is_active": True
    }
    response = await async_client.post("/auth/register/hr", json=hr_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == hr_data["email"]
    assert data["full_name"] == hr_data["full_name"]

    # 2. Login HR via /auth/login/hr
    login_data = {
        "email": "john.hr@company.com",
        "password": "secretpassword"
    }
    response = await async_client.post("/auth/login/hr", json=login_data)
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["role"] == "hr"
    token = token_data["access_token"]

    # 3. Get /auth/me with HR token
    headers = {"Authorization": f"Bearer {token}"}
    response = await async_client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    me_data = response.json()
    assert me_data["role"] == "hr"
    assert me_data["data"]["email"] == hr_data["email"]

    # 4. Register Applicant
    applicant_data = {
        "full_name": "Alice Applicant",
        "email": "alice.app@mail.com",
        "phone": "+123456789",
        "password": "applicantpassword"
    }
    response = await async_client.post("/auth/register/applicant", json=applicant_data)
    assert response.status_code == 200
    app_res = response.json()
    assert app_res["email"] == applicant_data["email"]

    # 5. Login Applicant via auto-detect /auth/login (without role)
    app_login_data = {
        "email": "alice.app@mail.com",
        "password": "applicantpassword"
    }
    response = await async_client.post("/auth/login", json=app_login_data)
    assert response.status_code == 200
    app_token_data = response.json()
    assert app_token_data["role"] == "applicant"
    app_token = app_token_data["access_token"]

    # 6. Get /auth/me with Applicant token
    app_headers = {"Authorization": f"Bearer {app_token}"}
    response = await async_client.get("/auth/me", headers=app_headers)
    assert response.status_code == 200
    app_me = response.json()
    assert app_me["role"] == "applicant"
    assert app_me["data"]["email"] == applicant_data["email"]

    # 7. Test invalid password login
    bad_login = {
        "email": "john.hr@company.com",
        "password": "wrongpassword",
        "role": "hr"
    }
    response = await async_client.post("/auth/login", json=bad_login)
    assert response.status_code == 401
