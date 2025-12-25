from services.CRUD import *
from models.models_dto import *
from services.monitoring import MonitoringService
from fastapi.security import HTTPBasicCredentials
from services.database import get_engine, get_session_fabric
from fastapi import APIRouter, HTTPException, status, Response, Depends, Query
from services.authorization import verify_user, security, level1, level2, level3



monitoring_api = APIRouter(prefix='/api', tags=['Monitoring'])



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



@monitoring_api.post("/monitoring", status_code=201)
async def create_indication_event_router(indication: CreateIndicationDTO, db: Session = Depends(get_db)):
    """Создание новых показаний и событий"""
    monitoring_services = MonitoringService(db)
    monitoring_services.process_indication(indication.sensor_id, indication.value)

    return {"Сообщение": f"Датчик с ID {indication.sensor_id} получил показание {indication.value}"}



@monitoring_api.get("/indication/sensor/{sensor_id}", response_model=List[IndicationDTO])
async def get_indications_by_sensor_id_router(sensor_id: int, user: User = Depends(authorization), db: Session = Depends(get_db)):
    """Получение всех показаний датчика"""
    company_id = get_room_by_id(db, get_sensor_by_id(db, sensor_id).room_id).company_id

    if (user.role not in level1) and ((user.role not in level3) or (user.company_id != company_id)):
        raise HTTPException(403, f"Необходимо:"
                                 f"\n- уровень доступа: {level1};"
                                 f"\n- уровень доступа: {level3} и быть сотрудником компании: {company_id}")

    return get_indications_by_sensor_id(db, sensor_id)



@monitoring_api.get("/event/sensor/{sensor_id}", response_model=List[EventDTO])
async def get_events_by_sensor_id_router(sensor_id: int, user: User = Depends(authorization), db: Session = Depends(get_db)):
    """Получение всех событий датчика"""
    company_id = get_room_by_id(db, get_sensor_by_id(db, sensor_id).room_id).company_id

    if (user.role not in level1) and ((user.role not in level3) or (user.company_id != company_id)):
        raise HTTPException(403, f"Необходимо:"
                                 f"\n- уровень доступа: {level1};"
                                 f"\n- уровень доступа: {level3} и быть сотрудником компании: {company_id}")

    return get_events_by_sensor_id(db, sensor_id)



@monitoring_api.put("/event/sensor/{sensor_id}", response_model=EventDTO)
async def update_event_by_sensor_id_router(sensor_id: int, event: UpdateEventDTO, user: User = Depends(authorization), db: Session = Depends(get_db)):
    """Обновление события по PK"""
    company_id = get_room_by_id(db, get_sensor_by_id(db, sensor_id).room_id).company_id
    if not company_id:
        raise HTTPException(404, f"Не удалось найти датчик с ID {sensor_id}")

    if (user.role not in level1) and ((user.role not in level2) or (user.company_id != company_id)):
        raise HTTPException(403, f"Необходимо:"
                                 f"\n- уровень доступа: {level1};"
                                 f"\n- уровень доступа: {level2} и быть сотрудником компании: {company_id}")

    result = get_last_event_by_sensor_id(db, sensor_id)
    if not result:
        raise HTTPException(404, f"Не удалось найти событие у датчика с ID {sensor_id}")

    update = update_event(db, sensor_id, result.time, event.eliminated, event.description)
    if not update:
        raise HTTPException(400, f"Не удалось обновить событие у датчика с ID {sensor_id}")

    db.refresh(result)
    return result
