from services.CRUD import *
from models.models_dto import *
from fastapi.security import HTTPBasicCredentials
from services.database import get_engine, get_session_fabric
from fastapi import APIRouter, HTTPException, status, Response, Depends, Query
from services.authorization import verify_user, security, level1, level2, level3



limitation_api = APIRouter(prefix='/api', tags=['Limitation'])



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



@limitation_api.post("/limitation", response_model=LimitationDTO, status_code=201)
async def create_limitation_router(limitation: LimitationDTO, user: User = Depends(authorization), db: Session = Depends(get_db)):
    """Создание нового ограничения"""
    if (user.role not in level1) and ((user.role not in level2) or (user.company_id != get_room_by_id(db, limitation.room_id).company_id)):
        raise HTTPException(403, f"Необходимо:"
                                 f"\n- уровень доступа: {level1};"
                                 f"\n- уровень доступа: {level2} и быть сотрудником компании: {get_room_by_id(db, limitation.room_id).company_id}")

    result = create_limitation(db, limitation.type, limitation.room_id, limitation.max, limitation.min)
    if not result:
        raise HTTPException(400, "Не удалось создать ограничение")

    return get_limitation_by_pk(db, limitation.type, limitation.room_id)



@limitation_api.get("/limitation/room/{room_id}", response_model=List[LimitationDTO])
async def get_limitations_by_room_id_router(room_id: int, user: User = Depends(authorization), db: Session = Depends(get_db)):
    """Получение всех ограничений помещения"""
    if (user.role not in level1) and ((user.role not in level3) or (user.company_id != get_room_by_id(db, room_id).company_id)):
        raise HTTPException(403, f"Необходимо:"
                                 f"\n- уровень доступа: {level1};"
                                 f"\n- уровень доступа: {level3} и быть сотрудником компании: {get_room_by_id(db, room_id).company_id}")

    return get_limitations_by_room_id(db, room_id)




@limitation_api.get("/limitation/{limitation_type}/{room_id}", response_model=LimitationDTO)
async def get_limitation_by_pk_router(limitation_type: str, room_id: int, user: User = Depends(authorization), db: Session = Depends(get_db)):
    """Получение ограничения по PK"""
    if user.role not in level3:
        raise HTTPException(403, f"Необходим уровень доступа: {level3}")

    result = get_limitation_by_pk(db, limitation_type, room_id)
    if not result:
        raise HTTPException(404, f"Не удалось найти ограничение с PK: {limitation_type}, {room_id}")

    if (user.role not in level1) and (user.company_id != get_room_by_id(db, result.room_id).company_id):
        raise HTTPException(403, f"Необходимо быть сотрудником компании: {get_room_by_id(db, result.room_id).company_id}")

    return result



@limitation_api.put("/limitation/{limitation_type}/{room_id}", response_model=LimitationDTO)
async def update_limitation_router(limitation_type: str, room_id: int, limitation: UpdateLimitationDTO, user: User = Depends(authorization), db: Session = Depends(get_db)):
    """Обновление ограничения по PK"""
    if user.role not in level2:
        raise HTTPException(403, f"Необходим уровень доступа: {level2}")

    result = get_limitation_by_pk(db, limitation_type, room_id)
    if not result:
        raise HTTPException(404, f"Не удалось найти ограничение с PK: {limitation_type}, {room_id}")

    if (user.role not in level1) and (user.company_id != get_room_by_id(db, result.room_id).company_id):
        raise HTTPException(403, f"Необходимо быть сотрудником компании: {get_room_by_id(db, result.room_id).company_id}")

    update = update_limitation(db, limitation_type, room_id, limitation.max, limitation.min)
    if not update:
        raise HTTPException(400, f"Не удалось обновить ограничение с PK: {limitation_type}, {room_id}")

    db.refresh(result)
    return result



@limitation_api.delete("/limitation/{limitation_type}/{room_id}")
async def delete_limitation_router(limitation_type: str, room_id: int, user: User = Depends(authorization), db: Session = Depends(get_db)):
    """Удаление ограничения по PK"""
    if user.role not in level2:
        raise HTTPException(403, f"Необходим уровень доступа: {level2}")

    result = get_limitation_by_pk(db, limitation_type, room_id)
    if not result:
        raise HTTPException(404, f"Не удалось найти ограничение с PK: {limitation_type}, {room_id}")

    if (user.role not in level1) and (user.company_id != get_room_by_id(db, result.room_id).company_id):
        raise HTTPException(403, f"Необходимо быть сотрудником компании: {get_room_by_id(db, result.room_id).company_id}")

    delete = delete_limitation(db, limitation_type, room_id)
    if not delete:
        raise HTTPException(400, f"Не удалось удалить ограничение с PK: {limitation_type}, {room_id}")

    return {"Сообщение": f"Ограничение с PK: {limitation_type}, {room_id} удалено"}
