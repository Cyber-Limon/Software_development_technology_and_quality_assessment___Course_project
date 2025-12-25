from datetime import datetime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, Enum, ForeignKey, UniqueConstraint



Base = declarative_base()

class Company(Base):
    __tablename__ = 'company'

    id      = Column(Integer,     primary_key=True, autoincrement=True)
    name    = Column(String(200), nullable=False)
    address = Column(String(500), nullable=False)

    room = relationship('Room', back_populates='company', cascade='all, delete-orphan')
    user = relationship('User', back_populates='company', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Предприятие(id={self.id}, Название={self.name}, Адрес={self.address})>"



class Room(Base):
    __tablename__ = 'room'

    id          = Column(Integer,     primary_key=True,         autoincrement=True)
    company_id  = Column(Integer,     ForeignKey('company.id'), nullable=False)
    number      = Column(Integer,     nullable=False)
    name        = Column(String(200), nullable=False)
    description = Column(String(500))

    __table_args__ = (UniqueConstraint('company_id', 'number', name='unique_room'),)

    company    = relationship('Company',    back_populates='room')
    sensor     = relationship('Sensor',     back_populates='room', cascade='all, delete-orphan')
    limitation = relationship('Limitation', back_populates='room', cascade='all, delete-orphan')

    def __repr__(self):
        return (f"<Помещение(id={self.id}, Предприятие_id={self.company.id}, Номер={self.number}), "
                f"Название={self.name}, Описание={self.description}>")



class User(Base):
    __tablename__ = 'user'

    id            = Column(Integer,     primary_key=True,         autoincrement=True)
    company_id    = Column(Integer,     ForeignKey('company.id'), nullable=False)
    code          = Column(Integer,     nullable=False)
    full_name     = Column(String(200), nullable=False)
    role          = Column(Enum('Администратор', 'Оператор', 'Пользователь', name='user_roles'), nullable=False)
    login         = Column(String(100), nullable=False,           unique=True)
    password_hash = Column(String(255), nullable=False)

    __table_args__ = (UniqueConstraint('company_id', 'code', name='unique_user'),)

    company = relationship('Company', back_populates='user')

    def __repr__(self):
        return (f"<Пользователь(id={self.id}, Предприятие_id={self.company.id}, Код={self.code}), "
                f"ФИО={self.full_name}, Логин={self.login}")



class Sensor(Base):
    __tablename__ = 'sensor'

    id      = Column(Integer,     primary_key=True,      autoincrement=True)
    room_id = Column(Integer,     ForeignKey('room.id'), nullable=False)
    type    = Column(String(100), nullable=False)
    active  = Column(Boolean,     nullable=False,        default=True)

    room       = relationship('Room',       back_populates='sensor')
    indication = relationship('Indication', back_populates='sensor', cascade='all, delete-orphan')
    event      = relationship('Event',      back_populates='sensor', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Датчик(id={self.id}, Помещение={self.room_id}, Тип={self.type}, Активен={self.active})>"



class Limitation(Base):
    __tablename__ = 'limitation'

    room_id = Column(Integer,     ForeignKey('room.id'), primary_key=True)
    type    = Column(String(100), primary_key=True)
    max     = Column(Integer,     nullable=False)
    min     = Column(Integer,     nullable=False)

    room = relationship('Room', back_populates='limitation')

    def __repr__(self):
        return (f"<Ограничение(Тип={self.type}, Помещение={self.room_id}, "
                f"Максимальное значение={self.max}), Минимальное значение={self.min}>")



class Indication(Base):
    __tablename__ = 'indication'

    sensor_id = Column(Integer,  ForeignKey('sensor.id'), primary_key=True)
    time      = Column(DateTime, primary_key=True,        default=datetime.now())
    value     = Column(Float,    nullable=False)
    status    = Column(Enum('Превышенное', 'Возможно превышение', 'Нормальное', name='indications_status'), nullable=False)

    sensor = relationship('Sensor', back_populates='indication')

    def __repr__(self):
        return (f"<Показание(Датчик_id={self.sensor_id}, Время={self.time}, "
                f"Значение={self.value}, Статус={self.status})>")



class Event(Base):
    __tablename__ = 'event'

    sensor_id   = Column(Integer,      ForeignKey('sensor.id'), primary_key=True)
    time        = Column(DateTime,     primary_key=True,        default=datetime.now())
    eliminated  = Column(Boolean,      nullable=False)
    description = Column(String(1000), nullable=False)

    sensor = relationship('Sensor', back_populates='event')

    def __repr__(self):
        return (f"<Событие(Датчик_id={self.sensor_id}, Время={self.time}, "
                f"Устранено={self.eliminated}, Описание={self.description})>")
