from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from services.CRUD import UserRoles, IndicationStatuses



# Company #

class CompanyDTO(BaseModel):
    id:      int
    name:    str
    address: str

    class Config:
        from_attributes = True


class CreateCompanyDTO(BaseModel):
    name:    str
    address: str


class UpdateCompanyDTO(BaseModel):
    name:    Optional[str] = None
    address: Optional[str] = None



# Room #

class RoomDTO(BaseModel):
    id:          int
    company_id:  int
    number:      int
    name:        str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class CreateRoomDTO(BaseModel):
    company_id:  int
    number:      int
    name:        str
    description: Optional[str]


class UpdateRoomDTO(BaseModel):
    number:      Optional[int] = None
    name:        Optional[str] = None
    description: Optional[str] = None



# User #

class UserDTO(BaseModel):
    id:         int
    company_id: int
    code:       int
    role:       UserRoles
    full_name:  str
    login:      str

    class Config:
        from_attributes = True


class CreateUserDTO(BaseModel):
    company_id: int
    code:       int
    role:       UserRoles
    full_name:  str
    login:      str
    password:   str


class UpdateUserDTO(BaseModel):
    code:      Optional[int]       = None
    role:      Optional[UserRoles] = None
    full_name: Optional[str]       = None
    login:     Optional[str]       = None
    password:  Optional[str]       = None



# Sensor #

class SensorDTO(BaseModel):
    id:      int
    room_id: int
    type:    str
    active:  bool

    class Config:
        from_attributes = True


class CreateSensorDTO(BaseModel):
    room_id: int
    type:    str
    active:  bool = True


class UpdateSensorDTO(BaseModel):
    room_id: Optional[int]  = None
    type:    Optional[str]  = None
    active:  Optional[bool] = None



# Limitation #

class LimitationDTO(BaseModel):
    type:    str
    room_id: int
    max:     int
    min:     int

    class Config:
        from_attributes = True


class UpdateLimitationDTO(BaseModel):
    max: Optional[int] = None
    min: Optional[int] = None



# Indication #

class IndicationDTO(BaseModel):
    sensor_id: int
    time:      datetime
    value:     float
    status:    IndicationStatuses

    class Config:
        from_attributes = True


class CreateIndicationDTO(BaseModel):
    sensor_id: int
    value:     float



# Event #

class EventDTO(BaseModel):
    sensor_id:   int
    time:        datetime
    eliminated:  bool
    description: str

    class Config:
        from_attributes = True


class CreateEventDTO(BaseModel):
    sensor_id:   int
    eliminated:  bool = False
    description: str


class UpdateEventDTO(BaseModel):
    eliminated:  Optional[bool] = None
    description: Optional[str]  = None
