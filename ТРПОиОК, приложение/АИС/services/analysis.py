from services.CRUD import *



class AnalysisService:
    def __init__(self, db: Session):
        self.db = db


    def cleaning(self, hour: int = 24):
        try:
            count = get_indications_count_by_less_hour(self.db, hour)
            delete_indications_by_less_hour(self.db, hour)

            print(f"Удалено старых показаний: {count} (старше {hour} часов)")
            return True

        except Exception as e:
            self.db.rollback()
            print(f"Ошибка очищения показаний датчиков: {e}")
            return False


    def forecast(self, sensor_id: int, value: float) -> float:
        indications = get_indications_by_sensor_id_and_more_hour(self.db, sensor_id, 3)

        values = [i.value for i in indications]
        values.append(value)

        if len(values) < 2:
            return value

        changes = []
        for i in range(1, len(values)):
            changes.append(values[i] - values[i - 1])

        avg_change = sum(changes) / len(changes)

        return round(values[-1] + avg_change * 60, 2)


    def analyze(self, sensor_id: int, value: float) -> dict:
        sensor = get_sensor_by_id(self.db, sensor_id)
        if not sensor:
            raise ValueError(f"Датчик с ID {sensor_id} не найден")

        limitation = get_limitation_by_pk(self.db, sensor.type, sensor.room_id)
        if not limitation:
            raise ValueError(f"Для датчика {sensor_id} (тип: {sensor.type}, помещение: {sensor.room_id}) не заданы ограничения")

        prediction = self.forecast(sensor_id, value)

        current_violation = (value < limitation.min or value > limitation.max)
        prediction_violation = (prediction < limitation.min or prediction > limitation.max)

        if current_violation:
            status = 'Превышенное'
        elif prediction_violation:
            status = 'Возможно превышение'
        else:
            status = 'Нормальное'

        return {
            'sensor_id': sensor_id,
            'status': status,
            'value': round(value, 2),
            'prediction': prediction,
            'current_violation': current_violation,
            'prediction_violation': prediction_violation,
            'limitation_min': limitation.min,
            'limitation_max': limitation.max,
            'sensor_type': sensor.type
        }
