from services.CRUD import *
from models.models_dto import *
from fastapi.security import HTTPBasicCredentials
from services.database import get_engine, get_session_fabric
from fastapi import APIRouter, HTTPException, status, Response, Depends, Query
from services.authorization import verify_user, security, level1, level2, level3



company_api = APIRouter(prefix='/api', tags=['Company'])



engine = get_engine()
SessionLocal = get_session_fabric(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()



def authorization(data: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)) -> User:
    return verify_user(data, db)



@company_api.post("/company", response_model=CompanyDTO, status_code=201)
async def create_company_router(company: CreateCompanyDTO, user: User = Depends(authorization), db: Session = Depends(get_db)):
    """Создание новой компании"""
    if user.role not in level1:
        raise HTTPException(403, f"Необходим уровень доступа: {level1}")

    result = create_company(db, company.name, company.address)
    if not result:
        raise HTTPException(400, "Не удалось создать компанию")

    return db.query(Company).order_by(Company.id.desc()).first()



@company_api.get("/company/{company_id}", response_model=CompanyDTO)
async def get_company_by_id_router(company_id: int, user: User = Depends(authorization), db: Session = Depends(get_db)):
    """Получение компании по ID"""
    if user.role not in level3:
        raise HTTPException(403, f"Необходим уровень доступа: {level3}")

    result = get_company_by_id(db, company_id)
    if not result:
        raise HTTPException(404, f"Не удалось найти компанию с ID {company_id}")

    return result



@company_api.get("/company", response_model=List[CompanyDTO])
async def get_companies_router(user: User = Depends(authorization), db: Session = Depends(get_db)):
    """Получение всех компаний"""
    if user.role not in level3:
        raise HTTPException(403, f"Необходим уровень доступа: {level3}")

    return get_companies(db)



@company_api.put("/company/{company_id}", response_model=CompanyDTO)
async def update_company_router(company_id: int, company: UpdateCompanyDTO, user: User = Depends(authorization), db: Session = Depends(get_db)):
    """Обновление компании по ID"""
    if user.role not in level1:
        raise HTTPException(403, f"Необходим уровень доступа: {level1}")

    if company_id == 1:
        raise HTTPException(403, f"Нельзя изменять компанию с ID: 1")

    result = get_company_by_id(db, company_id)
    if not result:
        raise HTTPException(404, f"Не удалось найти компанию с ID {company_id}")

    update = update_company(db, company_id, company.name, company.address)
    if not update:
        raise HTTPException(400, f"Не удалось обновить компанию с ID {company_id}")

    db.refresh(result)
    return result



@company_api.delete("/company/{company_id}")
async def delete_company_router(company_id: int, user: User = Depends(authorization), db: Session = Depends(get_db)):
    """Удаление компании по ID"""
    if user.role not in level1:
        raise HTTPException(403, f"Необходим уровень доступа: {level1}")

    if company_id == 1:
        raise HTTPException(403, f"Нельзя удалять компанию с ID: 1")

    result = get_company_by_id(db, company_id)
    if not result:
        raise HTTPException(404, f"Не удалось найти компанию с ID {company_id}")

    delete = delete_company(db, company_id)
    if not delete:
        raise HTTPException(400, f"Не удалось удалить компанию с ID {company_id}")

    return {"Сообщение": f"Компания с ID {company_id} удалена"}
