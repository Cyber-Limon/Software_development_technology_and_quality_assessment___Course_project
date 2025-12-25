from services.CRUD import *
from models.models_dto import *
from fastapi.security import HTTPBasicCredentials
from services.database import get_engine, get_session_fabric
from fastapi import APIRouter, HTTPException, status, Response, Depends, Query
from services.authorization import verify_user, security, level1, level2, level3



user_api = APIRouter(prefix='/api', tags=['User'])



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



@user_api.post("/user", response_model=UserDTO, status_code=201)
async def create_user_router(process_user: CreateUserDTO, user: User = Depends(authorization), db: Session = Depends(get_db)):
    """Создание нового пользователя"""
    if (user.role not in level1) and ((user.role not in level2) or (user.company_id != process_user.company_id)):
        raise HTTPException(403, f"Необходимо:"
                                 f"\n- уровень доступа: {level1};"
                                 f"\n- уровень доступа: {level2} и быть сотрудником компании: {process_user.company_id}")

    if process_user.company_id == 1:
        raise HTTPException(403, f"Нельзя добавлять пользователей в компанию с ID: 1")

    if process_user.role in level1:
        raise HTTPException(403, f"Нельзя создавать пользователя с уровнем: {level1}")

    result = create_user(db, process_user.company_id, process_user.code, process_user.full_name, process_user.role, process_user.login, process_user.password)
    if not result:
        raise HTTPException(400, "Не удалось создать пользователя")

    return db.query(User).order_by(User.id.desc()).first()



@user_api.get("/user/{user_id}", response_model=UserDTO)
async def get_user_by_id_router(user_id: int, user: User = Depends(authorization), db: Session = Depends(get_db)):
    """Получение пользователя по ID"""
    if user.role not in level3:
        raise HTTPException(403, f"Необходим уровень доступа: {level3}")

    result = get_user_by_id(db, user_id)
    if not result:
        raise HTTPException(404, f"Не удалось найти пользователя с ID {user_id}")

    if (user.role not in level1) and (user.company_id != result.company_id):
        raise HTTPException(403, f"Необходимо быть сотрудником компании: {result.company_id}")

    return result



@user_api.get("/user/company/{company_id}", response_model=List[UserDTO])
async def get_users_by_company_id_router(company_id: int, user: User = Depends(authorization), db: Session = Depends(get_db)):
    """Получение всех пользователей компаний"""
    if (user.role not in level1) and ((user.role not in level3) or (user.company_id != company_id)):
        raise HTTPException(403, f"Необходимо:"
                                 f"\n- уровень доступа: {level1};"
                                 f"\n- уровень доступа: {level3} и быть сотрудником компании: {company_id}")

    return get_users_by_company_id(db, company_id)



@user_api.put("/user/{user_id}", response_model=UserDTO)
async def update_user_router(user_id: int, process_user: UpdateUserDTO, user: User = Depends(authorization), db: Session = Depends(get_db)):
    """Обновление пользователя по ID"""
    if user.role not in level2:
        raise HTTPException(403, f"Необходим уровень доступа: {level2}")

    result = get_user_by_id(db, user_id)
    if not result:
        raise HTTPException(404, f"Не удалось найти пользователя с ID {user_id}")

    if (user.role not in level1) and (user.company_id != result.company_id):
        raise HTTPException(403, f"Необходимо быть сотрудником компании: {result.company_id}")

    if process_user.role in level1:
        raise HTTPException(403, f"Нельзя создавать пользователя с уровнем: {level1}")

    update = update_user(db, user_id, process_user.code, process_user.full_name, process_user.role, process_user.login, process_user.password)
    if not update:
        raise HTTPException(400, f"Не удалось обновить пользователя с ID {user_id}")

    db.refresh(result)
    return result



@user_api.delete("/user/{user_id}")
async def delete_user_router(user_id: int, user: User = Depends(authorization), db: Session = Depends(get_db)):
    """Удаление пользователя по ID"""
    if user.role not in level2:
        raise HTTPException(403, f"Необходим уровень доступа: {level2}")

    result = get_user_by_id(db, user_id)
    if not result:
        raise HTTPException(404, f"Не удалось найти пользователя с ID {user_id}")

    if (user.role not in level1) and (user.company_id != result.company_id):
        raise HTTPException(403, f"Необходимо быть сотрудником компании: {result.company_id}")

    delete = delete_user(db, user_id)
    if not delete:
        raise HTTPException(400, f"Не удалось удалить пользователя с ID {user_id}")

    return {"Сообщение": f"Пользователь с ID {user_id} удален"}
