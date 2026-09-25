import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI

sys.path.append(str(Path(__file__).resolve().parent.parent))

from hr_service.api.vacancy import router as vacancy_router
from hr_service.api.company import router as company_router
app = FastAPI()

app.include_router(vacancy_router)
app.include_router(company_router)

if __name__ == '__main__':
    uvicorn.run("hr_service.main:app", host='127.0.0.1', port=8000)
