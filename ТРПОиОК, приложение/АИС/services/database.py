import settings
import sqlalchemy
from typing import Optional
from models.models_dao import Base
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker



def get_engine(db_url: str = None, db_sync: bool = False) -> Optional[Engine]:
    try:
        if db_url is None:
            db_url = settings.DATABASE_URL

        engine = sqlalchemy.create_engine(url=db_url, echo=True)

        if db_sync:
            Base.metadata.create_all(bind=engine)
            print("Таблицы БД успешно созданы")
        return engine

    except Exception as error:
        print(f"Ошибка при создании движка БД: {error}")
        return None


def get_session_fabric(engine: Engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
