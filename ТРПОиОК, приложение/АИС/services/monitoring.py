from datetime import datetime
from sqlalchemy.orm import Session
from services.analysis import AnalysisService
from services.CRUD import create_indication, create_event, get_events_by_sensor_id



class MonitoringService:
    def __init__(self, db: Session):
        self.db = db
        self.cleaning_hour = None
        self.analysis = AnalysisService(db)


    def process_indication(self, sensor_id: int, value: float):
        try:
            analysis_result = self.analysis.analyze(sensor_id, value)

            create_indication(self.db, sensor_id, None, value, analysis_result['status'])

            self.cleanup()

            if analysis_result['current_violation']:
                self.create_event(sensor_id, value, analysis_result)

        except Exception as e:
            print(f"Ошибка при создании показания: {e}")
            self.db.rollback()


    def create_event(self, sensor_id: int, value: float, analysis: dict):
        try:
            event = get_events_by_sensor_id(self.db, sensor_id)

            if event and not event[-1].eliminated:
                return None

            if value < analysis['limitation_min']:
                comparison = "<"
            else:
                comparison = ">"

            description = (
                f"Показатель {analysis['sensor_type']} = {value} {comparison} нормы "
                f"(норма: {analysis['limitation_min']}-{analysis['limitation_max']})"
            )

            create_event(self.db, sensor_id, True, description)

        except Exception as e:
            print(f"Ошибка при создании события: {e}")
            return None


    def cleanup(self):
        try:
            current_hour = datetime.now().hour

            if self.cleaning_hour is None or current_hour != self.cleaning_hour:
                self.analysis.cleaning()
                self.cleaning_hour = current_hour

        except Exception as e:
            print(f"Ошибка при очистке данных: {e}")
