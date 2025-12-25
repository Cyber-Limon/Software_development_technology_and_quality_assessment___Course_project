import hashlib
import functools
import traceback
from models.models_dao import *
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, List, Literal



def dbexception(db_func):
    @functools.wraps(db_func)
    def decorated_func(db: Session, *args, **kwargs) -> bool:
        try:
            db_func(db, *args, **kwargs)
            db.commit()
            return True
        except:
            print(f'Исключение в {db_func.__name__}: {traceback.format_exc()}')
            db.rollback()
            return False
    return decorated_func


# Company #

@dbexception
def create_company(db: Session, name: str, address: str) -> bool:
    company = Company(name=name, address=address)
    db.add(company)


def get_company_by_id(db: Session, company_id: int) -> Optional[Company]:
    result = db.query(Company).get(company_id)
    return result


def get_companies(db: Session) -> List[Company]:
    result = db.query(Company).order_by(Company.id.asc()).all()
    return result


@dbexception
def update_company(db: Session, company_id: int, name: str = None, address: str = None) -> bool:
    company = get_company_by_id(db, company_id)

    if not company:
        print(f'Предупреждение: компания с ID {company_id} не найдена')
        return False

    if name is not None:
        company.name = name
    if address is not None:
        company.address = address


@dbexception
def delete_company(db: Session, company_id: int) -> bool:
    company = get_company_by_id(db, company_id)

    if not company:
        print(f'Предупреждение: компания с ID {company_id} не найдена')
        return False

    db.delete(company)



# Room #

@dbexception
def create_room(db: Session, company_id: int, number: int, name: str, description: str = None) -> bool:
    room = Room(company_id=company_id, number=number, name=name, description=description)
    db.add(room)


def get_room_by_id(db: Session, room_id: int) -> Optional[Room]:
    result = db.query(Room).get(room_id)
    return result


def get_rooms_by_company_id(db: Session, company_id: int) -> List[Room]:
    result = db.query(Room).filter(Room.company_id == company_id).all()
    return result


@dbexception
def update_room(db: Session, room_id: int, number: int = None, name: str = None, description: str = None) -> bool:
    room = get_room_by_id(db, room_id)

    if not room:
        print(f'Предупреждение: помещение с ID {room_id} не найдено')
        return False

    if number is not None:
        room.number = number
    if name is not None:
        room.name = name
    if description is not None:
        room.description = description


@dbexception
def delete_room(db: Session, room_id: int) -> bool:
    room = get_room_by_id(db, room_id)

    if not room:
        print(f'Предупреждение: помещение с ID {room_id} не найдено')
        return False

    db.delete(room)



# User #

UserRoles = Literal['Администратор', 'Оператор', 'Пользователь']

@dbexception
def create_user(db: Session, company_id: int, code: int, full_name: str, role: UserRoles, login: str, password: str) -> bool:
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    user = User(company_id=company_id, code=code, full_name=full_name, role=role, login=login, password_hash=password_hash)
    db.add(user)


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    result = db.query(User).get(user_id)
    return result


def get_user_by_login(db: Session, login: str) -> Optional[User]:
    result = db.query(User).filter(User.login == login).first()
    return result


def get_users_by_company_id(db: Session, company_id: int) -> List[User]:
    result = db.query(User).filter(User.company_id == company_id).all()
    return result


@dbexception
def update_user(db: Session, user_id: int, code: int = None, full_name: str = None, role: UserRoles = None,
                login: str = None, password: str = None) -> bool:
    user = get_user_by_id(db, user_id)

    if not user:
        print(f'Предупреждение: пользователь с ID {user_id} не найден')
        return False

    if code is not None:
        user.code = code
    if full_name is not None:
        user.full_name = full_name
    if role is not None:
        user.role = role
    if login is not None:
        user.login = login
    if password is not None:
        user.password_hash = hashlib.sha256(password.encode()).hexdigest()


@dbexception
def delete_user(db: Session, user_id: int) -> bool:
    user = get_user_by_id(db, user_id)

    if not user:
        print(f'Предупреждение: пользователь с ID {user_id} не найден')
        return False

    db.delete(user)



# Sensor #

@dbexception
def create_sensor(db: Session, room_id: int, sensor_type: str, active: bool) -> bool:
    sensor = Sensor(room_id=room_id, type=sensor_type, active=active)
    db.add(sensor)


def get_sensor_by_id(db: Session, sensor_id: int) -> Optional[Sensor]:
    result = db.query(Sensor).get(sensor_id)
    return result


def get_sensors_by_room_id(db: Session, room_id: int) -> List[Sensor]:
    result = db.query(Sensor).filter(Sensor.room_id == room_id).all()
    return result


@dbexception
def update_sensor(db: Session, sensor_id: int, room_id: int = None, sensor_type: str = None, active: bool = None) -> bool:
    sensor = get_sensor_by_id(db, sensor_id)

    if not sensor:
        print(f'Предупреждение: датчик с ID {sensor_id} не найден')
        return False

    if room_id is not None:
        sensor.room_id = room_id
    if sensor_type is not None:
        sensor.type = sensor_type
    if active is not None:
        sensor.active = active


@dbexception
def delete_sensor(db: Session, sensor_id: int) -> bool:
    sensor = get_sensor_by_id(db, sensor_id)

    if not sensor:
        print(f'Предупреждение: датчик с ID {sensor_id} не найден')
        return False

    db.delete(sensor)



# Limitation #

@dbexception
def create_limitation(db: Session, limitation_type: str, room_id: int, limitation_max: int, limitation_min: int) -> bool:
    limitation = get_limitation_by_pk(db, limitation_type, room_id)

    if limitation:
        print(f'Предупреждение: в помещении {room_id} ограничение {limitation_type} уже существует')

    limitation = Limitation(type=limitation_type, room_id=room_id, max=limitation_max, min=limitation_min)
    db.add(limitation)


def get_limitation_by_pk(db: Session, limitation_type: str, room_id: int) -> Optional[Limitation]:
    result = db.query(Limitation).filter(Limitation.type == limitation_type, Limitation.room_id == room_id).first()
    return result


def get_limitations_by_room_id(db: Session, room_id: int) -> List[Limitation]:
    result = db.query(Limitation).filter(Limitation.room_id == room_id).all()
    return result


@dbexception
def update_limitation(db: Session, limitation_type: str, room_id: int,
                      limitation_max: int = None, limitation_min: int = None) -> bool:
    limitation = get_limitation_by_pk(db, limitation_type, room_id)

    if not limitation:
        print(f'Предупреждение: в помещении {room_id} ограничение {limitation_type} не найдено')
        return False

    if limitation_max is not None:
        limitation.max = limitation_max
    if limitation_min is not None:
        limitation.min = limitation_min


@dbexception
def delete_limitation(db: Session, limitation_type: str, room_id: int) -> bool:
    limitation = get_limitation_by_pk(db, limitation_type, room_id)

    if not limitation:
        print(f'Предупреждение: в помещении {room_id} ограничение {limitation_type} не найдено')
        return False

    db.delete(limitation)



# Indication #

IndicationStatuses = Literal['Превышенное', 'Возможно превышение', 'Нормальное']

@dbexception
def create_indication(db: Session, sensor_id: int, time: Optional[datetime], value: float, status: IndicationStatuses) -> bool:
    indication = Indication(sensor_id=sensor_id, time=(time if time else datetime.now()), value=value, status=status)
    db.add(indication)


def get_indication_by_pk(db: Session, sensor_id: int, time: datetime) -> Optional[Indication]:
    result = db.query(Indication).filter(Indication.sensor_id == sensor_id, Indication.time == time).first()
    return result


def get_indications_by_sensor_id(db: Session, sensor_id: int) -> List[Indication]:
    result = db.query(Indication).filter(Indication.sensor_id == sensor_id).order_by(Indication.time.asc()).all()
    return result


def get_indications_by_sensor_id_and_more_hour(db: Session, sensor_id: int, hour: int) -> Optional[List]:
    required_time = datetime.now() - timedelta(hours=hour)

    result = (db.query(Indication).filter(Indication.sensor_id == sensor_id, Indication.time >= required_time).
              order_by(Indication.time.asc()).all())
    return result


def get_indications_count_by_less_hour(db: Session, hour: int) -> int:
    required_time = datetime.now() - timedelta(hours=hour)

    result = db.query(Indication).filter(Indication.time < required_time).count()
    return result


@dbexception
def delete_indication(db: Session, sensor_id: int, time: datetime) -> bool:
    indication = get_indication_by_pk(db, sensor_id, time)

    if not indication:
        print(f'Предупреждение: у датчика {sensor_id} нет показания в {time}')
        return False

    db.delete(indication)


@dbexception
def delete_indications_by_less_hour(db: Session, hour: int) -> bool:
    required_time = datetime.now() - timedelta(hours=hour)

    if get_indications_count_by_less_hour(db, hour) == 0:
        print(f'Предупреждение: показания старше {required_time} не найдены')
        return False

    db.query(Indication).filter(Indication.time < required_time).delete()




# Event #

@dbexception
def create_event(db: Session, sensor_id: int, eliminated: bool, description: str) -> bool:
    event = Event(sensor_id=sensor_id, time=datetime.now(), eliminated=eliminated, description=description)
    db.add(event)


def get_event_by_pk(db: Session, sensor_id: int, time: datetime) -> Optional[Event]:
    result = db.query(Event).filter(Event.sensor_id == sensor_id, Event.time == time).first()
    return result


def get_last_event_by_sensor_id(db: Session, sensor_id: int) -> Optional[Event]:
    result = db.query(Event).filter(Event.sensor_id == sensor_id).order_by(Event.time.desc()).first()
    return result


def get_events_by_sensor_id(db: Session, sensor_id: int) -> List[Event]:
    result = db.query(Event).filter(Event.sensor_id == sensor_id).order_by(Event.time.asc()).all()
    return result


@dbexception
def update_event(db: Session, sensor_id: int, time: datetime, eliminated: bool = None, description: str = None) -> bool:
    event = get_event_by_pk(db, sensor_id, time)

    if not event:
        print(f'Предупреждение: у датчика {sensor_id} событие за {time} не найдено')
        return False

    if eliminated is not None:
        event.eliminated = eliminated
    if description is not None:
        event.description = description


@dbexception
def delete_event(db: Session, sensor_id: int, time: datetime) -> bool:
    event = get_event_by_pk(db, sensor_id, time)

    if not event:
        print(f'Предупреждение: у датчика {sensor_id} событие за {time} не найдено')
        return False

    db.delete(event)
