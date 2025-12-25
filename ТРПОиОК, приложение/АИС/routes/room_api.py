from services.CRUD import *
from models.models_dto import *
from fastapi.security import HTTPBasicCredentials
from services.database import get_engine, get_session_fabric
from fastapi import APIRouter, HTTPException, status, Response, Depends, Query
from services.authorization import verify_user, security, level1, level2, level3



room_api = APIRouter(prefix='/api', tags=['Room'])



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



@room_api.post("/room", response_model=RoomDTO, status_code=201)
async def create_room_router(room: CreateRoomDTO, user: User = Depends(authorization), db: Session = Depends(get_db)):
    """Создание нового помещения"""
    if (user.role not in level1) and ((user.role not in level2) or (user.company_id != room.company_id)):
        raise HTTPException(403, f"Необходимо:"
                                 f"\n- уровень доступа: {level1};"
                                 f"\n- уровень доступа: {level2} и быть сотрудником компании: {room.company_id}")

    if room.company_id == 1:
        raise HTTPException(403, f"Нельзя добавлять помещения в компанию с ID: 1")

    result = create_room(db, room.company_id, room.number, room.name, room.description)
    if not result:
        raise HTTPException(400, "Не удалось создать помещение")

    return db.query(Room).order_by(Room.id.desc()).first()



@room_api.get("/room/{room_id}", response_model=RoomDTO)
async def get_room_by_id_router(room_id: int, user: User = Depends(authorization), db: Session = Depends(get_db)):
    """Получение помещения по ID"""
    if user.role not in level3:
        raise HTTPException(403, f"Необходим уровень доступа: {level3}")

    result = get_room_by_id(db, room_id)
    if not result:
        raise HTTPException(404, f"Не удалось найти помещение с ID {room_id}")

    if (user.role not in level1) and (user.company_id != result.company_id):
        raise HTTPException(403, f"Необходимо быть сотрудником компании: {result.company_id}")

    return result



@room_api.get("/room/company/{company_id}", response_model=List[RoomDTO])
async def get_rooms_by_company_id_router(company_id: int, user: User = Depends(authorization), db: Session = Depends(get_db)):
    """Получение всех помещений компаний"""
    if (user.role not in level1) and ((user.role not in level3) or (user.company_id != company_id)):
        raise HTTPException(403, f"Необходимо:"
                                 f"\n- уровень доступа: {level1};"
                                 f"\n- уровень доступа: {level3} и быть сотрудником компании: {company_id}")

    return get_rooms_by_company_id(db, company_id)



@room_api.put("/room/{room_id}", response_model=RoomDTO)
async def update_room_router(room_id: int, room: UpdateRoomDTO, user: User = Depends(authorization), db: Session = Depends(get_db)):
    """Обновление помещения по ID"""
    if user.role not in level2:
        raise HTTPException(403, f"Необходим уровень доступа: {level2}")

    result = get_room_by_id(db, room_id)
    if not result:
        raise HTTPException(404, f"Не удалось найти помещение с ID {room_id}")

    if (user.role not in level1) and (user.company_id != result.company_id):
        raise HTTPException(403, f"Необходимо быть сотрудником компании: {result.company_id}")

    update = update_room(db, room_id, room.number, room.name, room.description)
    if not update:
        raise HTTPException(400, f"Не удалось обновить комнату с ID {room_id}")

    db.refresh(result)
    return result



@room_api.delete("/room/{room_id}")
async def delete_room_router(room_id: int, user: User = Depends(authorization), db: Session = Depends(get_db)):
    """Удаление помещения по ID"""
    if user.role not in level2:
        raise HTTPException(403, f"Необходим уровень доступа: {level2}")

    result = get_room_by_id(db, room_id)
    if not result:
        raise HTTPException(404, f"Не удалось найти помещение с ID {room_id}")

    if (user.role not in level1) and (user.company_id != result.company_id):
        raise HTTPException(403, f"Необходимо быть сотрудником компании: {result.company_id}")

    delete = delete_room(db, room_id)
    if not delete:
        raise HTTPException(400, f"Не удалось удалить помещение с ID {room_id}")

    return {"Сообщение": f"Помещение с ID {room_id} удалено"}
