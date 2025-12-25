import time
import random
import models.models_dao as models
from CRUD import *
from monitoring import MonitoringService
from database import get_engine, get_session_fabric



def init_database():
    engine = get_engine(db_sync=True)
    if engine is None:
        print("Ошибка: не удалось создать движок БД")
        return None

    SessionLocal = get_session_fabric(engine)
    return SessionLocal()



def populate_test_data(db):
    create_company(db, "MAIN",       "-")
    create_company(db, "Компания 1", "г. Уфа")
    create_company(db, "Компания 2", "г. Уфа")

    companies = db.query(models.Company).all()
    company_main, company_1, company_2 = companies[0], companies[1], companies[2]



    create_room(db, company_1.id, 1, "Цех",         "Производственный цех с линией сборки")
    create_room(db, company_1.id, 2, "Склад",       "Складской комплекс")
    create_room(db, company_1.id, 3, "Лаборатория", "Контроль качества и испытания")
    create_room(db, company_2.id, 1, "Цех",         "Производственный цех с линией сборки")
    create_room(db, company_2.id, 2, "Склад",       "Складской комплекс")
    create_room(db, company_2.id, 3, "Лаборатория", "Контроль качества и испытания")

    rooms = db.query(models.Room).all()
    room_1_1, room_1_2, room_1_3 = rooms[0], rooms[1], rooms[2]
    room_2_1, room_2_2, room_2_3 = rooms[3], rooms[4], rooms[5]



    create_user(db, company_main.id, 1, "Иванов И.И.", "Администратор", "admin",     "admin")
    create_user(db, company_1.id,    1, "Иванов И.И.", "Оператор",      "operator1", "operator1")
    create_user(db, company_1.id,    2, "Иванов И.И.", "Пользователь",  "user1",     "user1")
    create_user(db, company_2.id,    1, "Иванов И.И.", "Оператор",      "operator2", "operator2")
    create_user(db, company_2.id,    2, "Иванов И.И.", "Пользователь",  "user2",     "user2")



    create_sensor(db, room_1_1.id, "Температура",   True)
    create_sensor(db, room_1_1.id, "Влажность",     True)
    create_sensor(db, room_1_1.id, "Задымленность", True)
    create_sensor(db, room_1_2.id, "Температура",   True)
    create_sensor(db, room_1_2.id, "Влажность",     True)
    create_sensor(db, room_1_2.id, "Задымленность", True)
    create_sensor(db, room_1_3.id, "Температура",   True)
    create_sensor(db, room_1_3.id, "Влажность",     True)
    create_sensor(db, room_1_3.id, "Задымленность", True)

    create_sensor(db, room_2_1.id, "Температура",   True)
    create_sensor(db, room_2_1.id, "Влажность",     True)
    create_sensor(db, room_2_1.id, "Задымленность", True)
    create_sensor(db, room_2_2.id, "Температура",   True)
    create_sensor(db, room_2_2.id, "Влажность",     True)
    create_sensor(db, room_2_2.id, "Задымленность", True)
    create_sensor(db, room_2_3.id, "Температура",   True)
    create_sensor(db, room_2_3.id, "Влажность",     True)
    create_sensor(db, room_2_3.id, "Задымленность", True)

    sensors = db.query(models.Sensor).all()



    create_limitation(db, "Температура",   room_1_1.id, 40, 10)
    create_limitation(db, "Влажность",     room_1_1.id, 80, 20)
    create_limitation(db, "Задымленность", room_1_1.id, 20, 0)
    create_limitation(db, "Температура",   room_1_2.id, 40, 10)
    create_limitation(db, "Влажность",     room_1_2.id, 80, 20)
    create_limitation(db, "Задымленность", room_1_2.id, 20, 0)
    create_limitation(db, "Температура",   room_1_3.id, 40, 10)
    create_limitation(db, "Влажность",     room_1_3.id, 80, 20)
    create_limitation(db, "Задымленность", room_1_3.id, 20, 0)
    create_limitation(db, "Температура",   room_2_1.id, 40, 10)
    create_limitation(db, "Влажность",     room_2_1.id, 80, 20)
    create_limitation(db, "Задымленность", room_2_1.id, 20, 0)
    create_limitation(db, "Температура",   room_2_2.id, 40, 10)
    create_limitation(db, "Влажность",     room_2_2.id, 80, 20)
    create_limitation(db, "Задымленность", room_2_2.id, 20, 0)
    create_limitation(db, "Температура",   room_2_3.id, 40, 10)
    create_limitation(db, "Влажность",     room_2_3.id, 80, 20)
    create_limitation(db, "Задымленность", room_2_3.id, 20, 0)



    monitoring_services = MonitoringService(db)

    for minute in range(60):
        for sensor in sensors:
            sensor_type = sensor.type

            base_value = 30.0 if sensor_type == "Влажность" else 20.0
            value = base_value + random.randint(-20, 20)
            monitoring_services.process_indication(sensor.id, value)
        time.sleep(1)



def main():
    db = init_database()
    if db is None:
        return

    try:
        populate_test_data(db)
        db.commit()

        print("\nБаза данных заполнена:")
        print(f"    Компаний: {db.query(models.Company).count()}")
        print(f"    Помещений: {db.query(models.Room).count()}")
        print(f"    Пользователей: {db.query(models.User).count()}")
        print(f"    Датчиков: {db.query(models.Sensor).count()}")
        print(f"    Ограничений {db.query(models.Limitation).count()}")
        print(f"    Показаний: {db.query(models.Indication).count()}")
        print(f"    Событий: {db.query(models.Event).count()}")

    except Exception as e:
        db.rollback()
        print(f"\nОшибка при заполнении БД: {e}")
        import traceback
        traceback.print_exc()

    finally:
        db.close()
        print("\nCкрипт завершен.")



if __name__ == "__main__":
    main()
