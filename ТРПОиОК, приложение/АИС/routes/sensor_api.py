from services.CRUD import *
from models.models_dto import *
from fastapi.security import HTTPBasicCredentials
from services.database import get_engine, get_session_fabric
from fastapi import APIRouter, HTTPException, status, Response, Depends, Query
from services.authorization import verify_user, security, level1, level2, level3



sensor_api = APIRouter(prefix='/api', tags=['Sensor'])



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



@sensor_api.post("/sensor", response_model=SensorDTO, status_code=201)
async def create_sensor_router(sensor: CreateSensorDTO, user: User = Depends(authorization), db: Session = Depends(get_db)):
    """Создание нового датчика"""
    if (user.role not in level1) and ((user.role not in level2) or (user.company_id != get_room_by_id(db, sensor.room_id).company_id)):
        raise HTTPException(403, f"Необходимо:"
                                 f"\n- уровень доступа: {level1};"
                                 f"\n- уровень доступа: {level2} и быть сотрудником компании: {get_room_by_id(db, sensor.room_id).company_id}")

    result = create_sensor(db, sensor.room_id, sensor.type, True)
    if not result:
        raise HTTPException(400, "Не удалось создать датчик")

    return db.query(Sensor).order_by(Sensor.id.desc()).first()



@sensor_api.get("/sensor/{sensor_id}", response_model=SensorDTO)
async def get_sensor_by_id_router(sensor_id: int, user: User = Depends(authorization), db: Session = Depends(get_db)):
    """Получение датчика по ID"""
    if user.role not in level3:
        raise HTTPException(403, f"Необходим уровень доступа: {level3}")

    result = get_sensor_by_id(db, sensor_id)
    if not result:
        raise HTTPException(404, f"Не удалось найти датчик с ID {sensor_id}")

    if (user.role not in level1) and (user.company_id != get_room_by_id(db, result.room_id).company_id):
        raise HTTPException(403, f"Необходимо быть сотрудником компании: {get_room_by_id(db, result.room_id).company_id}")

    return result



@sensor_api.get("/sensor/room/{room_id}", response_model=List[SensorDTO])
async def get_sensors_by_room_id_router(room_id: int, user: User = Depends(authorization), db: Session = Depends(get_db)):
    """Получение всех датчиков помещения"""
    if (user.role not in level1) and ((user.role not in level3) or (user.company_id != get_room_by_id(db, room_id).company_id)):
        raise HTTPException(403, f"Необходимо:"
                                 f"\n- уровень доступа: {level1};"
                                 f"\n- уровень доступа: {level3} и быть сотрудником компании: {get_room_by_id(db, room_id).company_id}")

    return get_sensors_by_room_id(db, room_id)



@sensor_api.put("/sensor/{sensor_id}", response_model=SensorDTO)
async def update_sensor_router(sensor_id: int, sensor: UpdateSensorDTO, user: User = Depends(authorization), db: Session = Depends(get_db)):
    """Обновление датчика по ID"""
    if user.role not in level2:
        raise HTTPException(403, f"Необходим уровень доступа: {level2}")

    result = get_sensor_by_id(db, sensor_id)
    if not result:
        raise HTTPException(404, f"Не удалось найти датчик с ID {sensor_id}")

    if (user.role not in level1) and (user.company_id != get_room_by_id(db, result.room_id).company_id):
        raise HTTPException(403, f"Необходимо быть сотрудником компании: {get_room_by_id(db, result.room_id).company_id}")

    if get_room_by_id(db, sensor.room_id).company_id != get_room_by_id(db, result.room_id).company_id:
        raise HTTPException(409, f"Нельзя менять помещения на те, которые не принадлежат компании с ID: {get_room_by_id(db, result.room_id).company_id}")

    update = update_sensor(db, sensor_id, sensor.room_id, sensor.type, sensor.active)
    if not update:
        raise HTTPException(400, f"Не удалось обновить датчик с ID {sensor_id}")

    db.refresh(result)
    return result



@sensor_api.delete("/sensor/{sensor_id}")
async def delete_sensor_router(sensor_id: int, user: User = Depends(authorization), db: Session = Depends(get_db)):
    """Удаление датчика по ID"""
    if user.role not in level2:
        raise HTTPException(403, f"Необходим уровень доступа: {level2}")

    result = get_sensor_by_id(db, sensor_id)
    if not result:
        raise HTTPException(404, f"Не удалось найти датчик с ID {sensor_id}")

    if (user.role not in level1) and (user.company_id != get_room_by_id(db, result.room_id).company_id):
        raise HTTPException(403, f"Необходимо быть сотрудником компании: {get_room_by_id(db, result.room_id).company_id}")

    delete = delete_sensor(db, sensor_id)
    if not delete:
        raise HTTPException(400, f"Не удалось удалить датчик с ID {sensor_id}")

    return {"Сообщение": f"Датчик с ID {sensor_id} удален"}
