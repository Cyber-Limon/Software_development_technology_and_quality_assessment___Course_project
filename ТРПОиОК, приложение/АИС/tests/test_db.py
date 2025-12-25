import hashlib
import unittest
from services.CRUD import *
from datetime import datetime, timedelta
from services.analysis import AnalysisService
from services.monitoring import MonitoringService
from services.database import get_engine, get_session_fabric



class TestCompanyCRUD(unittest.TestCase):
    def setUp(self):
        self.engine = get_engine(db_url='sqlite:///:memory:', db_sync=True)
        SessionLocal = get_session_fabric(self.engine)
        self.db = SessionLocal()


    def tearDown(self):
        self.db.close()


    def test_create_and_get(self):
        success = create_company(self.db, "Компания", "Адрес")
        self.assertTrue(success)

        company = get_company_by_id(self.db, 1)
        self.assertIsNotNone(company)
        self.assertEqual(company.name, "Компания")
        self.assertEqual(company.address, "Адрес")


    def test_update(self):
        create_company(self.db, "Компания_с", "Адрес_с")

        success = update_company(self.db, 1, "Компания_н", "Адрес_н")
        self.assertTrue(success)

        company = get_company_by_id(self.db, 1)
        self.assertEqual(company.name, "Компания_н")
        self.assertEqual(company.address, "Адрес_н")


    def test_delete(self):
        create_company(self.db, "Компания", "Адрес")

        success = delete_company(self.db, 1)
        self.assertTrue(success)

        company = get_company_by_id(self.db, 1)
        self.assertIsNone(company)


    def test_get_nonexistent(self):
        company = get_company_by_id(self.db, 999)
        self.assertIsNone(company)


    def test_update_nonexistent(self):
        success = update_company(self.db, 999, "Компания", "Адрес")
        self.assertTrue(success)


    def test_delete_nonexistent(self):
        success = delete_company(self.db, 999)
        self.assertTrue(success)



class TestRoomCRUD(unittest.TestCase):
    def setUp(self):
        self.engine = get_engine(db_url='sqlite:///:memory:', db_sync=True)
        SessionLocal = get_session_fabric(self.engine)
        self.db = SessionLocal()

        create_company(self.db, "Компания", "Адрес")


    def tearDown(self):
        self.db.close()


    def test_create_and_get(self):
        success = create_room(self.db, 1, 1, "Помещение", "Описание")
        self.assertTrue(success)

        room = get_room_by_id(self.db, 1)
        self.assertIsNotNone(room)
        self.assertEqual(room.number, 1)
        self.assertEqual(room.name, "Помещение")
        self.assertEqual(room.description, "Описание")
        self.assertEqual(room.company_id, 1)


    def test_update(self):
        create_room(self.db, 1, 1, "Помещение_с", "Описание_с")

        success = update_room(self.db, 1, 2, "Помещение_н", "Описание_н")
        self.assertTrue(success)

        room = get_room_by_id(self.db, 1)
        self.assertEqual(room.number, 2)
        self.assertEqual(room.name, "Помещение_н")
        self.assertEqual(room.description, "Описание_н")


    def test_delete(self):
        create_room(self.db, 1, 1, "Помещение", "Описание")

        success = delete_room(self.db, 1)
        self.assertTrue(success)

        room = get_room_by_id(self.db, 1)
        self.assertIsNone(room)


    def test_get_nonexistent(self):
        room = get_room_by_id(self.db, 999)
        self.assertIsNone(room)


    def test_update_nonexistent(self):
        success = update_room(self.db, 999, name="Помещение")
        self.assertTrue(success)


    def test_delete_nonexistent(self):
        success = delete_room(self.db, 999)
        self.assertTrue(success)



class TestUserCRUD(unittest.TestCase):
    def setUp(self):
        self.engine = get_engine(db_url='sqlite:///:memory:', db_sync=True)
        SessionLocal = get_session_fabric(self.engine)
        self.db = SessionLocal()

        create_company(self.db, "Компания", "Адрес")


    def tearDown(self):
        self.db.close()


    def test_create_and_get(self):
        success = create_user(self.db, 1, 1, "ФИО", "Администратор", "login", "password")
        self.assertTrue(success)

        user = get_user_by_id(self.db, 1)
        self.assertIsNotNone(user)
        self.assertEqual(user.code, 1)
        self.assertEqual(user.full_name, "ФИО")
        self.assertEqual(user.login, "login")
        self.assertEqual(user.role, "Администратор")
        self.assertEqual(user.password_hash, hashlib.sha256("password".encode()).hexdigest())
        self.assertEqual(user.company_id, 1)


    def test_update(self):
        create_user(self.db, 1, 1, "ФИО_с", "Пользователь", "login_с", "password_с")

        success = update_user(self.db, 1, 2, "ФИО_н", "Оператор", "login_н", "password_н")
        self.assertTrue(success)

        user = get_user_by_id(self.db, 1)
        self.assertEqual(user.code, 2)
        self.assertEqual(user.full_name, "ФИО_н")
        self.assertEqual(user.role, "Оператор")
        self.assertEqual(user.login, "login_н")
        self.assertEqual(user.password_hash, hashlib.sha256("password_н".encode()).hexdigest())


    def test_delete(self):
        create_user(self.db, 1, 1, "ФИО", "Администратор", "login", "password")

        success = delete_user(self.db, 1)
        self.assertTrue(success)

        user = get_user_by_id(self.db, 1)
        self.assertIsNone(user)


    def test_get_nonexistent(self):
        user = get_user_by_id(self.db, 999)
        self.assertIsNone(user)


    def test_update_nonexistent(self):
        success = update_user(self.db, 999, full_name="ФИО")
        self.assertTrue(success)


    def test_delete_nonexistent(self):
        success = delete_user(self.db, 999)
        self.assertTrue(success)



class TestAnalysis(unittest.TestCase):
    def setUp(self):
        self.engine = get_engine(db_url='sqlite:///:memory:', db_sync=True)
        SessionLocal = get_session_fabric(self.engine)
        self.db = SessionLocal()

        create_company(self.db, "Компания", "Адрес")
        create_room(self.db, 1, 1, "Помещение", "Описание")
        create_sensor(self.db, 1, "Температура", True)
        create_limitation(self.db, "Температура", 1, 40, 10)

        base_time = datetime.now() - timedelta(hours=3)
        for i in range(1, 11):
            create_indication(self.db, 1, base_time + timedelta(minutes=i), 20.0 + i * 0.5, "Нормальное")

        self.analysis = AnalysisService(self.db)


    def tearDown(self):
        self.db.close()


    def test_cleaning(self):
        create_indication(self.db, 1, datetime.now() - timedelta(hours=25), 25, "Нормальное")

        count_before = self.db.query(Indication).count()

        success = self.analysis.cleaning()
        self.assertTrue(success)

        count_after = self.db.query(Indication).count()
        self.assertEqual(count_after, count_before - 1)


    def test_get_indications_by_sensor_id_and_more_hour(self):
        indications = get_indications_by_sensor_id_and_more_hour(self.db, 1, 3)

        values = [i.value for i in indications]
        self.assertEqual(len(values), 10)
        self.assertGreater(values[-1], values[0])


    def test_forecast(self):
        value = 20.0 + 11 * 0.5

        prediction = self.analysis.forecast(1, value)
        self.assertIsInstance(prediction, float)

        expected = value + 30
        self.assertAlmostEqual(prediction, expected, delta=0.1)


    def test_forecast_nonexistent(self):
        create_sensor(self.db, 1, "Влажность", True)

        prediction = self.analysis.forecast(2, 0.0)
        self.assertEqual(prediction, 0.0)


    def test_analyze_indication_normal(self):
        result = self.analysis.analyze(1, 20.0)
        self.assertEqual(result['sensor_id'], 1)
        self.assertEqual(result['status'], 'Нормальное')
        self.assertEqual(result['value'], 20.0)
        self.assertFalse(result['current_violation'])
        self.assertFalse(result['prediction_violation'])
        self.assertEqual(result['limitation_min'], 10)
        self.assertEqual(result['limitation_max'], 40)
        self.assertEqual(result['sensor_type'], 'Температура')


    def test_analyze_indication_prediction_violation(self):
        result = self.analysis.analyze(1, 25.0)
        self.assertEqual(result['status'], 'Возможно превышение')
        self.assertTrue(result['prediction_violation'])


    def test_analyze_indication_current_violation(self):
        result = self.analysis.analyze(1, 45.0)
        self.assertEqual(result['status'], 'Превышенное')
        self.assertTrue(result['current_violation'])


    def test_analyze_no_sensor(self):
        with self.assertRaises(ValueError) as context:
            self.analysis.analyze(999, 25.0)
        self.assertIn("Датчик с ID 999 не найден", str(context.exception))


    def test_analyze_no_limitations(self):
        create_sensor(self.db, 1, "Давление", True)

        with self.assertRaises(ValueError) as context:
            self.analysis.analyze(sensor_id=2, value=25.0)
        self.assertIn("не заданы ограничения", str(context.exception))



class TestMonitoring(unittest.TestCase):
    def setUp(self):
        self.engine = get_engine(db_url='sqlite:///:memory:', db_sync=True)
        SessionLocal = get_session_fabric(self.engine)
        self.db = SessionLocal()

        create_company(self.db, "Компания", "Адрес")
        create_room(self.db, 1, 1, "Помещение", "Описание")
        create_sensor(self.db, 1, "Температура", True)
        create_limitation(self.db, "Температура", 1, 40, 10)

        base_time = datetime.now() - timedelta(hours=3)
        for i in range(1, 11):
            create_indication(self.db, 1, base_time + timedelta(minutes=i), 20.0 + i * 0.5, "Нормальное")

        self.monitoring = MonitoringService(self.db)


    def tearDown(self):
        self.db.close()


    def test_process_indication(self):
        self.monitoring.process_indication(1, 45)

        indications = get_indications_by_sensor_id(self.db, 1)
        events = get_events_by_sensor_id(self.db, 1)

        self.assertEqual(len([i for i in indications]), 11)
        self.assertEqual(len([i for i in events]), 1)


    def test_cleanup_delete(self):
        old_time = datetime.now() - timedelta(hours=25)
        create_indication(self.db, 1, old_time, 25.0, "Нормальное")

        fresh_time = datetime.now() - timedelta(hours=1)
        create_indication(self.db, 1, fresh_time, 30.0, "Нормальное")

        count_before = self.db.query(Indication).count()

        self.monitoring.cleanup()

        count_after = self.db.query(Indication).count()
        self.assertEqual(count_after, count_before - 1)

        indication = get_indication_by_pk(self.db, 1, fresh_time)
        self.assertIsNotNone(indication)
        self.assertEqual(indication.value, 30.0)


    def test_cleanup_periodicity(self):
        self.monitoring.cleanup()

        time = datetime.now() - timedelta(hours=25)
        create_indication(self.db, 1, time, 25.0, "Нормальное")

        self.monitoring.cleanup()

        indication = get_indication_by_pk(self.db, 1, time)
        self.assertIsNotNone(indication)
        self.assertEqual(indication.value, 25.0)



if __name__ == '__main__':
    unittest.main()
