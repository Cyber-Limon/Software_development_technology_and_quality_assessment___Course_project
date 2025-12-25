import hashlib
from fastapi import HTTPException
from models.models_dao import User
from sqlalchemy.orm import Session
from services.CRUD import get_user_by_login
from services.database import get_session_fabric, get_engine
from fastapi.security import HTTPBasic, HTTPBasicCredentials



engine = get_engine()
SessionLocal = get_session_fabric(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



security = HTTPBasic()

def verify_user(data: HTTPBasicCredentials, db: Session) -> User:
    user = get_user_by_login(db, data.username)
    if not user or user.password_hash != hashlib.sha256(data.password.encode()).hexdigest():
        raise HTTPException(401, "Неверный логин или пароль")

    return user



level1 = ["Администратор"]
level2 = ["Администратор", "Оператор"]
level3 = ["Администратор", "Оператор", "Пользователь"]
