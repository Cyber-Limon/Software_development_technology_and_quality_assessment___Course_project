import React, { useState } from 'react';
import api from '../services/api';
import IndicationChart from './IndicationChart';

const IndicationsWithChart = () => {
  const [indications, setIndications] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filterSensorId, setFilterSensorId] = useState('');
  const [sensorInfo, setSensorInfo] = useState(null);
  const [limitations, setLimitations] = useState(null);

  // Загрузка показаний
  const loadIndications = async (sensorId) => {
    if (!sensorId) {
      alert('Введите ID датчика для загрузки показаний');
      return;
    }
    
    setLoading(true);
    try {
      // Загружаем показания
      const response = await api.get(`/api/indication/sensor/${sensorId}`);
      setIndications(response.data);
      
      // Загружаем информацию о датчике
      try {
        const sensorRes = await api.get(`/api/sensor/${sensorId}`);
        setSensorInfo(sensorRes.data);
        
        // Загружаем ограничения для этого датчика
        if (sensorRes.data.room_id) {
          const limitRes = await api.get(`/api/limitation/room/${sensorRes.data.room_id}`);
          const sensorLimits = limitRes.data.find(limit => limit.type === sensorRes.data.type);
          setLimitations(sensorLimits);
        }
      } catch (err) {
        console.error('Ошибка загрузки информации о датчике:', err);
        setSensorInfo(null);
        setLimitations(null);
      }
      
    } catch (error) {
      console.error('Ошибка загрузки показаний:', error);
      alert(`Ошибка: ${error.message}`);
      setIndications([]);
      setSensorInfo(null);
      setLimitations(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {/* Фильтр */}
      <div className="uk-card uk-card-default uk-card-body uk-margin-bottom">
        <h3 className="uk-card-title">Показания с графиком</h3>
        <div className="uk-flex uk-flex-middle">
          <div className="uk-margin-right">
            <label className="uk-form-label">ID датчика:</label>
            <input
              className="uk-input uk-form-width-small"
              type="number"
              value={filterSensorId}
              onChange={(e) => setFilterSensorId(e.target.value)}
              placeholder="ID датчика"
              min="1"
            />
          </div>
          <button 
            className="uk-button uk-button-primary"
            onClick={() => loadIndications(filterSensorId)}
            disabled={loading || !filterSensorId}
          >
            {loading ? (
              <>
                <span className="uk-margin-small-right" uk-spinner="ratio: 0.5"></span>
                Загрузка...
              </>
            ) : (
              'Загрузить'
            )}
          </button>
          
          {sensorInfo && (
            <div className="uk-margin-left uk-text-meta">
              Датчик: <strong>{sensorInfo.type}</strong> 
              {sensorInfo.room_id && ` (Комната: ${sensorInfo.room_id})`}
              {sensorInfo.active ? ' Активен' : '  Не активен'}
            </div>
          )}
        </div>
        
        {/* Информация об ограничениях */}
        {limitations && (
          <div className="uk-alert-primary uk-margin-top" uk-alert>
            <p>
              <strong>Ограничения для этого датчика:</strong><br/>
              Минимальное значение: <strong>{limitations.min}</strong><br/>
              Максимальное значение: <strong>{limitations.max}</strong>
            </p>
          </div>
        )}
      </div>

      {/* Таблица показаний (простая, без EntitySection) */}
      {indications.length > 0 && (
        <div className="uk-card uk-card-default uk-card-body uk-margin-bottom">
          <div className="uk-flex uk-flex-between uk-flex-middle">
            <h4 className="uk-card-title">Показания (таблица)</h4>
            <button 
              className="uk-button uk-button-secondary uk-button-small"
              onClick={() => loadIndications(filterSensorId)}
              disabled={loading}
            >
              <span uk-icon="refresh"></span> Обновить
            </button>
          </div>
          
          <div className="uk-overflow-auto">
            <table className="uk-table uk-table-small uk-table-divider uk-table-hover">
              <thead>
                <tr>
                  <th>ДАТЧИК</th>
                  <th>ВРЕМЯ</th>
                  <th>ЗНАЧЕНИЕ</th>
                  <th>СТАТУС</th>
                </tr>
              </thead>
              <tbody>
                {indications.map((item, index) => (
                  <tr key={index}>
                    <td>{item.sensor_id}</td>
                    <td>{new Date(item.time).toLocaleString()}</td>
                    <td>{item.value.toFixed(2)}</td>
                    <td>
                      <span className={`uk-label ${
                        item.status === 'Нормальное' ? 'uk-label-success' :
                        item.status === 'Возможно превышение' ? 'uk-label-warning' :
                        'uk-label-danger'
                      }`}>
                        {item.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <div className="uk-text-meta uk-text-center uk-margin-top">
              Показано записей: {indications.length}
            </div>
          </div>
        </div>
      )}

      {/* График */}
      {indications.length > 0 && (
        <div className="uk-margin-top">
          <IndicationChart 
            data={indications}
            sensorType={sensorInfo?.type || 'Датчик'}
            sensorId={filterSensorId}
            minLimit={limitations?.min}
            maxLimit={limitations?.max}
          />
        </div>
      )}

      {/* Сообщение если нет данных */}
      {!loading && indications.length === 0 && filterSensorId && (
        <div className="uk-alert-warning uk-margin-top" uk-alert>
          <p>Нет показаний для датчика с ID: {filterSensorId}. Проверьте ID датчика.</p>
        </div>
      )}
    </div>
  );
};

export default IndicationsWithChart;