import asyncio
import sys
from pathlib import Path

# Add hr_service to path

from hr_service.database import async_session
from hr_service.models.company import Company
from hr_service.models.vacancy import Vacancy
from hr_service.models.applicant import Applicant
from hr_service.utils.auth_utils import hash_password

COMPANY_PREFIXES = ["Техно", "Софт", "Диджитал", "Групп", "Системс", "Лаб", "Инновации", "Дата", "Смарт", "Веб"]
COMPANY_ROOTS = ["Альфа", "Бета", "Гамма", "Дельта", "Омега", "Прайм", "Атлас", "Вектор", "Квант", "Нейро", "Стандарт", "Про", "Мега", "Ультра", "Солар", "Арктик", "Сириус", "Феникс", "Титан", "Зенит"]

FIRST_NAMES = ["Александр", "Максим", "Иван", "Артем", "Дмитрий", "Никита", "Михаил", "Даниил", "Егор", "Андрей", "Евгений", "Сергей", "Алексей", "Илья", "Кирилл", "Владимир", "Павел", "Роман", "Денис", "Виктор"]
LAST_NAMES = ["Иванов", "Смирнов", "Кузнецов", "Попов", "Васильев", "Петров", "Соколов", "Михайлов", "Федоров", "Морозов", "Волков", "Алексеев", "Лебедев", "Семенов", "Егоров", "Павлов", "Козлов", "Степанов", "Николаев", "Орлов"]

JOB_POSITIONS = [
    {"title": "Senior Python Developer", "stack": "Python, FastAPI, PostgreSQL, Docker, Redis", "exp": 3.0, "req": "Опыт разработки на Python от 3 лет, знание FastAPI, асинхронного программирования и работы с БД.", "salary": 300000},
    {"title": "Frontend React Engineer", "stack": "JavaScript, TypeScript, React, Redux, Tailwind", "exp": 2.5, "req": "Уверенное знание TypeScript, React, опыт оптимизации веб-приложений и работы со стейт-менеджерами.", "salary": 260000},
    {"title": "DevOps Engineer", "stack": "Kubernetes, Docker, Terraform, CI/CD, AWS/Yandex Cloud", "exp": 3.0, "req": "Опыт построения CI/CD пайплайнов, администрирования Kubernetes и облачной инфраструктуры.", "salary": 320000},
    {"title": "Data Scientist / AI Engineer", "stack": "Python, PyTorch, LangChain, Transformers, OpenAI API", "exp": 2.0, "req": "Опыт работы с LLM, RAG, дообучением нейросетей и векторными базами данных.", "salary": 350000},
    {"title": "QA Automation Engineer", "stack": "Python, Pytest, Selenium, Allure, API Testing", "exp": 2.0, "req": "Опыт автоматизации тестирования REST API и веб-интерфейсов, знание Python и Pytest.", "salary": 220000}
]

async def seed():
    print("🌱 Начинаем заполнение базы данных тестовыми данными...")
    async with async_session() as session:
        # 1. Create 50 Companies
        print("Создание 50 компаний...")
        companies = []
        for i in range(50):
            root = COMPANY_ROOTS[i % len(COMPANY_ROOTS)]
            pref = COMPANY_PREFIXES[i % len(COMPANY_PREFIXES)]
            title = f"ООО «{root}{pref}» #{i+1}"
            desc = f"Ведущая технологическая компания #{i+1}, специализирующаяся на разработке масштабируемых ИТ-продуктов и облачных решений."
            company = Company(title=title, description=desc, is_active=True)
            session.add(company)
            companies.append(company)
        await session.commit()
        
        # Refresh companies to get IDs
        for c in companies:
            await session.refresh(c)
        print(f"✅ Успешно создано компаний: {len(companies)}")

        # 2. Create Vacancies for each company (2-3 vacancies per company)
        print("Создание вакансий для компаний...")
        vacancy_count = 0
        for company in companies:
            # Pick 2 or 3 jobs for this company
            num_vacancies = (company.id.int % 2) + 2
            for j in range(num_vacancies):
                job = JOB_POSITIONS[(company.id.int + j) % len(JOB_POSITIONS)]
                vacancy = Vacancy(
                    title=f"{job['title']} ({company.title.split()[0]})",
                    stack=job["stack"],
                    experience=job["exp"],
                    requirements=job["req"],
                    salary=job["salary"] + ((j * 15000) % 100000),
                    is_active=True,
                    company_id=company.id
                )
                session.add(vacancy)
                vacancy_count += 1
        await session.commit()
        print(f"✅ Успешно создано вакансий: {vacancy_count}")

        # 3. Create 250 Applicants
        print("Создание 250 соискателей...")
        hashed_pw = hash_password("password123")
        applicants_created = 0
        
        for i in range(250):
            fname = FIRST_NAMES[i % len(FIRST_NAMES)]
            lname = LAST_NAMES[(i * 7) % len(LAST_NAMES)]
            full_name = f"{fname} {lname} {i+1}"
            email = f"applicant.test.{i+1}@mail.com"
            phone = f"+7 (9{i%10}0) {100+i%899}-{i%90+10}-{i%90+10}"
            
            # Check if applicant already exists
            existing = await session.run_sync(lambda s: s.query(Applicant).filter_by(email=email).first())
            if not existing:
                applicant = Applicant(
                    full_name=full_name,
                    email=email,
                    hashed_password=hashed_pw,
                    phone=phone,
                    resume_path=f"company/mock/applications/resume_{i+1}.pdf"
                )
                session.add(applicant)
                applicants_created += 1

        await session.commit()
        print(f"✅ Успешно создано соискателей: {applicants_created}")
        print("🎉 Заполнение базы данных завершено успешно!")


