import React, { useState, useEffect } from 'react';
import api from '../services/api';
import EntitySection from './EntitySection';
import IndicationsWithChart from './IndicationsWithChart';

const Dashboard = () => {
  const [companies, setCompanies] = useState([]);
  const [rooms, setRooms] = useState([]);
  const [users, setUsers] = useState([]);
  const [sensors, setSensors] = useState([]);
  const [limitations, setLimitations] = useState([]);
  const [events, setEvents] = useState([]);

  const [loading, setLoading] = useState({
    companies: false,
    rooms: false,
    users: false,
    sensors: false,
    limitations: false,
    events: false
  });

  // Загрузка компаний
  const loadCompanies = async () => {
    setLoading(prev => ({ ...prev, companies: true }));
    try {
      const response = await api.get('/api/company');
      setCompanies(response.data);
    } catch (error) {
      console.error('Ошибка загрузки компаний:', error);
    } finally {
      setLoading(prev => ({ ...prev, companies: false }));
    }
  };

  // Загрузка помещений по ID компании
  const loadRooms = async (companyId) => {
    if (!companyId) {
      alert('Введите ID компании для загрузки помещений');
      return;
    }
    
    setLoading(prev => ({ ...prev, rooms: true }));
    try {
      const response = await api.get(`/api/room/company/${companyId}`);
      setRooms(response.data);
    } catch (error) {
      console.error('Ошибка загрузки помещений:', error);
      alert(`Ошибка: ${error.message}`);
    } finally {
      setLoading(prev => ({ ...prev, rooms: false }));
    }
  };

  // Загрузка пользователей по ID компании
  const loadUsers = async (companyId) => {
    if (!companyId) {
      alert('Введите ID компании для загрузки пользователей');
      return;
    }
    
    setLoading(prev => ({ ...prev, users: true }));
    try {
      const response = await api.get(`/api/user/company/${companyId}`);
      setUsers(response.data);
    } catch (error) {
      console.error('Ошибка загрузки пользователей:', error);
      alert(`Ошибка: ${error.message}`);
    } finally {
      setLoading(prev => ({ ...prev, users: false }));
    }
  };

  // Загрузка датчиков по ID помещения
  const loadSensors = async (roomId) => {
    if (!roomId) {
      alert('Введите ID помещения для загрузки датчиков');
      return;
    }
    
    setLoading(prev => ({ ...prev, sensors: true }));
    try {
      const response = await api.get(`/api/sensor/room/${roomId}`);
      setSensors(response.data);
    } catch (error) {
      console.error('Ошибка загрузки датчиков:', error);
      alert(`Ошибка: ${error.message}`);
    } finally {
      setLoading(prev => ({ ...prev, sensors: false }));
    }
  };

  // Загрузка ограничений по ID помещения
  const loadLimitations = async (roomId) => {
    if (!roomId) {
      alert('Введите ID помещения для загрузки ограничений');
      return;
    }
    
    setLoading(prev => ({ ...prev, limitations: true }));
    try {
      const response = await api.get(`/api/limitation/room/${roomId}`);
      setLimitations(response.data);
    } catch (error) {
      console.error('Ошибка загрузки ограничений:', error);
      alert(`Ошибка: ${error.message}`);
    } finally {
      setLoading(prev => ({ ...prev, limitations: false }));
    }
  };

  // Загрузка событий по ID датчика
  const loadEvents = async (sensorId) => {
    if (!sensorId) {
      alert('Введите ID датчика для загрузки событий');
      return;
    }
    
    setLoading(prev => ({ ...prev, events: true }));
    try {
      const response = await api.get(`/api/event/sensor/${sensorId}`);
      setEvents(response.data);
    } catch (error) {
      console.error('Ошибка загрузки событий:', error);
      alert(`Ошибка: ${error.message}`);
    } finally {
      setLoading(prev => ({ ...prev, events: false }));
    }
  };

  // Загружаем компании при старте
  useEffect(() => {
    loadCompanies();
  }, []);

  // Функции CRUD
  const entityConfigs = {
    companies: {
      title: 'Компании',
      data: companies,
      loading: loading.companies,
      fields: ['id', 'name', 'address'],
      create: async (data) => {
        await api.post('/api/company', data);
        loadCompanies();
      },
      update: async (id, data) => {
        await api.put(`/api/company/${id}`, data);
        loadCompanies();
      },
      delete: async (id) => {
        await api.delete(`/api/company/${id}`);
        loadCompanies();
      }
    },
    rooms: {
      title: 'Помещения',
      data: rooms,
      loading: loading.rooms,
      fields: ['id', 'company_id', 'number', 'name', 'description'],
      create: async (data) => {
        await api.post('/api/room', data);
        // После создания загружаем помещения для этой компании
        if (data.company_id) {
          loadRooms(data.company_id);
        }
      },
      update: async (id, data) => {
        await api.put(`/api/room/${id}`, data);
        // Перезагружаем помещения для той же компании
        const room = rooms.find(r => r.id === id);
        if (room && room.company_id) {
          loadRooms(room.company_id);
        }
      },
      delete: async (id) => {
        const room = rooms.find(r => r.id === id);
        await api.delete(`/api/room/${id}`);
        if (room && room.company_id) {
          loadRooms(room.company_id);
        }
      }
    },
    users: {
      title: 'Пользователи',
      data: users,
      loading: loading.users,
      fields: ['id', 'company_id', 'code', 'full_name', 'role', 'login'],
      create: async (data) => {
        await api.post('/api/user', data);
        if (data.company_id) {
          loadUsers(data.company_id);
        }
      },
      update: async (id, data) => {
        await api.put(`/api/user/${id}`, data);
        const user = users.find(u => u.id === id);
        if (user && user.company_id) {
          loadUsers(user.company_id);
        }
      },
      delete: async (id) => {
        const user = users.find(u => u.id === id);
        await api.delete(`/api/user/${id}`);
        if (user && user.company_id) {
          loadUsers(user.company_id);
        }
      }
    },
    sensors: {
      title: 'Датчики',
      data: sensors,
      loading: loading.sensors,
      fields: ['id', 'room_id', 'type', 'active'],
      create: async (data) => {
        await api.post('/api/sensor', data);
        if (data.room_id) {
          loadSensors(data.room_id);
        }
      },
      update: async (id, data) => {
        await api.put(`/api/sensor/${id}`, data);
        const sensor = sensors.find(s => s.id === id);
        if (sensor && sensor.room_id) {
          loadSensors(sensor.room_id);
        }
      },
      delete: async (id) => {
        const sensor = sensors.find(s => s.id === id);
        await api.delete(`/api/sensor/${id}`);
        if (sensor && sensor.room_id) {
          loadSensors(sensor.room_id);
        }
      }
    },
    limitations: {
      title: 'Ограничения',
      data: limitations,
      loading: loading.limitations,
      fields: ['type', 'room_id', 'max', 'min'],
      create: async (data) => {
        await api.post('/api/limitation', data);
        if (data.room_id) {
          loadLimitations(data.room_id);
        }
      },
      update: async (type, roomId, data) => {
        await api.put(`/api/limitation/${type}/${roomId}`, data);
        loadLimitations(roomId);
      },
      delete: async (type, roomId) => {
        await api.delete(`/api/limitation/${type}/${roomId}`);
        loadLimitations(roomId);
      }
    },
    events: {
      title: 'События',
      data: events,
      loading: loading.events,
      fields: ['sensor_id', 'time', 'eliminated', 'description'],
      update: async (sensorId, time, data) => {
        await api.put(`/api/event/sensor/${sensorId}`, {
          ...data,
          time: time
        });
        loadEvents(sensorId);
      }
    }
  };

  return (
    <div className="uk-container uk-container-expand uk-margin-top">
      <div className="uk-grid uk-grid-small" data-uk-grid>
        <div className="uk-width-1-1">
          <div className="uk-card uk-card-default uk-card-body">
            <h1 className="uk-card-title">Система контроля и управления датчиками</h1>
            <p>
              Для загрузки данных введите ID в поле фильтрации и нажмите "Обновить" в соответствующей секции.
            </p>
            
            <div className="uk-alert-primary" uk-alert>
              <p>
                <strong>Как использовать:</strong><br/>
                1. В таблице "Компании" найдите нужный ID компании<br/>
                2. Введите этот ID в поле фильтрации в секциях "Помещения" или "Пользователи"<br/>
                3. В "Помещениях" найдите ID помещения<br/>
                4. Введите этот ID в секциях "Датчики" или "Ограничения"<br/>
                5. В "Датчиках" найдите ID датчика<br/>
                6. Введите этот ID в секциях "Показания" или "События"
              </p>
            </div>
          </div>
        </div>

        {/* Секции для сущностей с таблицами */}
        {Object.entries(entityConfigs).map(([key, config]) => (
          <div key={key} className="uk-width-1-1 uk-margin-top">
            <EntitySection
              entityKey={key}
              title={config.title}
              data={config.data}
              loading={config.loading}
              fields={config.fields}
              create={config.create}
              update={config.update}
              delete={config.delete}
              readOnly={config.readOnly}
              onRefresh={(filterId) => {
                // Вызываем соответствующую функцию загрузки с переданным ID
                switch(key) {
                  case 'companies':
                    loadCompanies();
                    break;
                  case 'rooms':
                    loadRooms(filterId);
                    break;
                  case 'users':
                    loadUsers(filterId);
                    break;
                  case 'sensors':
                    loadSensors(filterId);
                    break;
                  case 'limitations':
                    loadLimitations(filterId);
                    break;
                  case 'events':
                    loadEvents(filterId);
                    break;
                  default:
                    console.log('Неизвестная сущность:', key);
                }
              }}
            />
          </div>
        ))}

        {/* Секция "Показания" с графиком - отдельный компонент */}
        <div className="uk-width-1-1 uk-margin-top">
          <IndicationsWithChart />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;