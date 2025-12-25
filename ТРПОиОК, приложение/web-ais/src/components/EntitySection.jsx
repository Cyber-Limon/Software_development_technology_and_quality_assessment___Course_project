import React, { useState } from 'react';

const EntitySection = ({ 
  entityKey,
  title, 
  data, 
  loading, 
  fields, 
  create, 
  update, 
  delete: deleteFunc,
  readOnly = false,
  onRefresh 
}) => {
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);
  const [formData, setFormData] = useState({});
  
  // Поля для фильтрации
  const [filterCompanyId, setFilterCompanyId] = useState('');
  const [filterRoomId, setFilterRoomId] = useState('');
  const [filterSensorId, setFilterSensorId] = useState('');

  // Определяем, какие поля фильтрации нужны для этой сущности
  const getFilterFields = () => {
    switch(entityKey) {
      case 'rooms':
      case 'users':
        return (
          <div className="uk-margin">
            <label className="uk-form-label">ID компании для фильтрации:</label>
            <div className="uk-form-controls">
              <input
                className="uk-input uk-form-width-small"
                type="number"
                value={filterCompanyId}
                onChange={(e) => setFilterCompanyId(e.target.value)}
                placeholder="ID компании"
              />
            </div>
          </div>
        );
      case 'sensors':
      case 'limitations':
        return (
          <div className="uk-margin">
            <label className="uk-form-label">ID помещения для фильтрации:</label>
            <div className="uk-form-controls">
              <input
                className="uk-input uk-form-width-small"
                type="number"
                value={filterRoomId}
                onChange={(e) => setFilterRoomId(e.target.value)}
                placeholder="ID помещения"
              />
            </div>
          </div>
        );
      case 'indications':
      case 'events':
        return (
          <div className="uk-margin">
            <label className="uk-form-label">ID датчика для фильтрации:</label>
            <div className="uk-form-controls">
              <input
                className="uk-input uk-form-width-small"
                type="number"
                value={filterSensorId}
                onChange={(e) => setFilterSensorId(e.target.value)}
                placeholder="ID датчика"
              />
            </div>
          </div>
        );
      default:
        return null;
    }
  };

  // Получаем параметр фильтрации для кнопки "Обновить"
  const getFilterParam = () => {
    switch(entityKey) {
      case 'rooms':
      case 'users':
        return filterCompanyId || '';
      case 'sensors':
      case 'limitations':
        return filterRoomId || '';
      case 'indications':
      case 'events':
        return filterSensorId || '';
      default:
        return '';
    }
  };

  // Обработчик создания
  const handleCreate = async () => {
    try {
      // Преобразуем типы данных перед отправкой
      const processedData = { ...formData };
      
      // Преобразование числовых полей
      if (entityKey === 'rooms' || entityKey === 'users') {
        processedData.company_id = parseInt(processedData.company_id) || 0;
      }
      if (entityKey === 'sensors' || entityKey === 'limitations') {
        processedData.room_id = parseInt(processedData.room_id) || 0;
      }
      if (entityKey === 'users') {
        processedData.code = parseInt(processedData.code) || 0;
      }
      if (entityKey === 'limitations') {
        processedData.max = parseInt(processedData.max) || 0;
        processedData.min = parseInt(processedData.min) || 0;
      }
      
      // Преобразование boolean полей
      if (entityKey === 'sensors' && processedData.active !== undefined) {
        processedData.active = processedData.active === 'true';
      }
      
      await create(processedData);
      setShowCreateModal(false);
      setFormData({});
      onRefresh(getFilterParam());
    } catch (error) {
      alert(`Ошибка создания: ${error.message}`);
    }
  };

  // Обработчик обновления
  const handleUpdate = async () => {
    try {
      // Преобразуем типы данных перед отправкой
      const processedData = { ...formData };
      
      // Преобразование числовых полей
      if (entityKey === 'users' && processedData.code !== undefined) {
        processedData.code = parseInt(processedData.code);
      }
      if (entityKey === 'limitations') {
        if (processedData.max !== undefined) processedData.max = parseInt(processedData.max);
        if (processedData.min !== undefined) processedData.min = parseInt(processedData.min);
      }
      
      // Преобразование boolean полей
      if (entityKey === 'sensors' && processedData.active !== undefined) {
        processedData.active = processedData.active === 'true';
      }
      if (entityKey === 'events' && processedData.eliminated !== undefined) {
        processedData.eliminated = processedData.eliminated === 'true';
      }
      
      if (entityKey === 'limitations') {
        await update(selectedItem.type, selectedItem.room_id, processedData);
      } else if (entityKey === 'events') {
        await update(selectedItem.sensor_id, selectedItem.time, processedData);
      } else {
        await update(selectedItem.id, processedData);
      }
      setShowEditModal(false);
      setSelectedItem(null);
      setFormData({});
      onRefresh(getFilterParam());
    } catch (error) {
      alert(`Ошибка обновления: ${error.message}`);
    }
  };

  // Обработчик удаления
  const handleDelete = async () => {
    try {
      if (entityKey === 'limitations') {
        await deleteFunc(selectedItem.type, selectedItem.room_id);
      } else {
        await deleteFunc(selectedItem.id);
      }
      setShowDeleteModal(false);
      setSelectedItem(null);
      onRefresh(getFilterParam());
    } catch (error) {
      alert(`Ошибка удаления: ${error.message}`);
    }
  };

  // Обработчик изменения полей формы
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  // Открытие модалки редактирования
  const openEditModal = (item) => {
    setSelectedItem(item);
    
    // Преобразуем данные для формы
    const formDataForEdit = { ...item };
    
    // Преобразуем boolean значения в строки для селектов
    if (entityKey === 'sensors') {
      formDataForEdit.active = item.active ? 'true' : 'false';
    }
    if (entityKey === 'events') {
      formDataForEdit.eliminated = item.eliminated ? 'true' : 'false';
    }
    
    setFormData(formDataForEdit);
    setShowEditModal(true);
  };

  // Открытие модалки удаления
  const openDeleteModal = (item) => {
    setSelectedItem(item);
    setShowDeleteModal(true);
  };

  // Определение кнопок в зависимости от сущности
  const showButtons = {
    create: !readOnly && create,
    update: !readOnly && update,
    delete: !readOnly && deleteFunc
  };

  // Функция для определения полей для создания
  const getCreateFieldsConfig = () => {
    switch(entityKey) {
      case 'companies':
        return [
          { field: 'name', label: 'Название', type: 'text', required: true },
          { field: 'address', label: 'Адрес', type: 'text', required: true }
        ];
      case 'users':
        return [
          { field: 'company_id', label: 'ID компании', type: 'number', required: true },
          { field: 'code', label: 'Код', type: 'number', required: true },
          { field: 'full_name', label: 'Полное имя', type: 'text', required: true },
          { field: 'login', label: 'Логин', type: 'text', required: true },
          { field: 'password', label: 'Пароль', type: 'password', required: true },
          { field: 'role', label: 'Роль', type: 'select', required: true,
            options: ['Администратор', 'Оператор', 'Пользователь'] }
        ];
      case 'rooms':
        return [
          { field: 'company_id', label: 'ID компании', type: 'number', required: true },
          { field: 'number', label: 'Номер', type: 'number', required: true },
          { field: 'name', label: 'Название', type: 'text', required: true },
          { field: 'description', label: 'Описание', type: 'text', required: false }
        ];
      case 'sensors':
        return [
          { field: 'room_id', label: 'ID помещения', type: 'number', required: true },
          { field: 'type', label: 'Тип', type: 'select', required: true,
            options: ['Температура', 'Влажность', 'Задымленность'] },
          { field: 'active', label: 'Активен', type: 'select', required: false,
            options: [{value: 'true', label: 'Активен'}, {value: 'false', label: 'Не активен'}] }
        ];
      case 'limitations':
        return [
          { field: 'type', label: 'Тип', type: 'select', required: true,
            options: ['Температура', 'Влажность', 'Задымленность'] },
          { field: 'room_id', label: 'ID помещения', type: 'number', required: true },
          { field: 'max', label: 'Максимум', type: 'number', required: true },
          { field: 'min', label: 'Минимум', type: 'number', required: true }
        ];
      case 'events':
        return [
          { field: 'sensor_id', label: 'ID датчика', type: 'number', required: true },
          { field: 'description', label: 'Описание', type: 'text', required: true },
          { field: 'eliminated', label: 'Устранено', type: 'select', required: false,
            options: [{value: 'false', label: 'Не устранено'}, {value: 'true', label: 'Устранено'}] }
        ];
      case 'indications':
        return [
          { field: 'sensor_id', label: 'ID датчика', type: 'number', required: true },
          { field: 'value', label: 'Значение', type: 'number', required: true }
        ];
      default:
        return [];
    }
  };

  // Функция для определения полей для редактирования
  const getEditFieldsConfig = () => {
    switch(entityKey) {
      case 'companies':
        return [
          { field: 'name', label: 'Название', type: 'text', disabled: false },
          { field: 'address', label: 'Адрес', type: 'text', disabled: false }
        ];
      case 'users':
        return [
          { field: 'code', label: 'Код', type: 'number', disabled: false },
          { field: 'full_name', label: 'Полное имя', type: 'text', disabled: false },
          { field: 'login', label: 'Логин', type: 'text', disabled: false },
          { field: 'password', label: 'Пароль', type: 'password', disabled: false },
          { field: 'role', label: 'Роль', type: 'select', disabled: false,
            options: ['Администратор', 'Оператор', 'Пользователь'] }
        ];
      case 'rooms':
        return [
          { field: 'number', label: 'Номер', type: 'number', disabled: false },
          { field: 'name', label: 'Название', type: 'text', disabled: false },
          { field: 'description', label: 'Описание', type: 'text', disabled: false }
        ];
      case 'sensors':
        return [
          { field: 'room_id', label: 'ID помещения', type: 'number', disabled: false },
          { field: 'type', label: 'Тип', type: 'select', disabled: false,
            options: ['Температура', 'Влажность', 'Задымленность'] },
          { field: 'active', label: 'Активен', type: 'select', disabled: false,
            options: [{value: 'true', label: 'Активен'}, {value: 'false', label: 'Не активен'}] }
        ];
      case 'limitations':
        return [
          { field: 'max', label: 'Максимум', type: 'number', disabled: false },
          { field: 'min', label: 'Минимум', type: 'number', disabled: false }
        ];
      case 'events':
        return [
          { field: 'eliminated', label: 'Устранено', type: 'select', disabled: false,
            options: [{value: 'false', label: 'Не устранено'}, {value: 'true', label: 'Устранено'}] },
          { field: 'description', label: 'Описание', type: 'text', disabled: false }
        ];
      case 'indications':
        // Показания нельзя редактировать через API
        return [];
      default:
        return [];
    }
  };

  // Рендер поля формы
  const renderField = (fieldConfig, isEdit = false) => {
    const { field, label, type, required = false, disabled = false, options } = fieldConfig;
    const value = formData[field] || '';
    
    if (type === 'select') {
      return (
        <div key={field} className="uk-margin">
          <label className="uk-form-label">
            {label}{required ? ' *' : ''}
          </label>
          <div className="uk-form-controls">
            <select
              className="uk-select"
              name={field}
              value={value}
              onChange={handleInputChange}
              required={required}
              disabled={disabled || (isEdit && field === 'company_id' && entityKey === 'users') || 
                               (isEdit && field === 'company_id' && entityKey === 'rooms') ||
                               (isEdit && field === 'room_id' && entityKey === 'limitations') ||
                               (isEdit && field === 'type' && entityKey === 'limitations') ||
                               (isEdit && field === 'sensor_id' && entityKey === 'events') ||
                               (isEdit && field === 'time' && entityKey === 'events')}
            >
              <option value="">Выберите...</option>
              {options.map(option => {
                if (typeof option === 'object') {
                  return <option key={option.value} value={option.value}>{option.label}</option>;
                } else {
                  return <option key={option} value={option}>{option}</option>;
                }
              })}
            </select>
          </div>
        </div>
      );
    }
    
    return (
      <div key={field} className="uk-margin">
        <label className="uk-form-label">
          {label}{required ? ' *' : ''}
        </label>
        <div className="uk-form-controls">
          <input
            className="uk-input"
            type={type}
            name={field}
            value={value}
            onChange={handleInputChange}
            placeholder={`Введите ${label.toLowerCase()}`}
            required={required}
            disabled={disabled || (isEdit && field === 'company_id' && entityKey === 'users') || 
                             (isEdit && field === 'company_id' && entityKey === 'rooms') ||
                             (isEdit && field === 'room_id' && entityKey === 'limitations') ||
                             (isEdit && field === 'type' && entityKey === 'limitations') ||
                             (isEdit && field === 'sensor_id' && entityKey === 'events') ||
                             (isEdit && field === 'time' && entityKey === 'events')}
          />
        </div>
      </div>
    );
  };

  return (
    <div className="uk-card uk-card-default uk-card-body">
      <div className="uk-flex uk-flex-between uk-flex-middle">
        <h3 className="uk-card-title">{title}</h3>
        <div className="uk-flex uk-flex-middle">
          {/* Поле фильтрации */}
          {getFilterFields()}
          
          <button 
            className="uk-button uk-button-secondary uk-button-small uk-margin-left"
            onClick={() => onRefresh(getFilterParam())}
            disabled={loading}
          >
            <span uk-icon="refresh"></span> Обновить
          </button>
          
          {showButtons.create && (
            <button 
              className="uk-button uk-button-primary uk-button-small uk-margin-left"
              onClick={() => setShowCreateModal(true)}
            >
              <span uk-icon="plus"></span> Добавить
            </button>
          )}
        </div>
      </div>

      {/* Информация о фильтрации */}
      {getFilterParam() && (
        <div className="uk-alert-primary uk-margin-small-top" uk-alert>
          <p>Фильтрация по: {getFilterParam()}</p>
        </div>
      )}

      {/* Таблица данных */}
      {loading ? (
        <div className="uk-text-center uk-padding">
          <span uk-spinner="ratio: 1.5"></span>
          <p>Загрузка...</p>
        </div>
      ) : data.length === 0 ? (
        <div className="uk-alert-warning uk-margin-top" uk-alert>
          <p>Нет данных для отображения. {getFilterParam() ? 'Проверьте фильтр.' : 'Загрузите данные.'}</p>
        </div>
      ) : (
        <div className="uk-overflow-auto uk-margin-top">
          <table className="uk-table uk-table-small uk-table-divider uk-table-hover">
            <thead>
              <tr>
                {fields.map(field => (
                  <th key={field}>{field.replace('_', ' ').toUpperCase()}</th>
                ))}
                {!readOnly && (showButtons.update || showButtons.delete) && (
                  <th>Действия</th>
                )}
              </tr>
            </thead>
            <tbody>
              {data.map((item, index) => (
                <tr key={index}>
                  {fields.map(field => (
                    <td key={field}>
                      {field === 'active' ? (
                        <span className={`uk-label ${item[field] ? 'uk-label-success' : 'uk-label-danger'}`}>
                          {item[field] ? 'АКТИВЕН' : 'НЕАКТИВЕН'}
                        </span>
                      ) : field === 'eliminated' ? (
                        <span className={`uk-label ${item[field] ? 'uk-label-success' : 'uk-label-warning'}`}>
                          {item[field] ? 'УСТРАНЕНО' : 'НЕ УСТРАНЕНО'}
                        </span>
                      ) : (
                        item[field]?.toString() || '-'
                      )}
                    </td>
                  ))}
                  {!readOnly && (showButtons.update || showButtons.delete) && (
                    <td>
                      {showButtons.update && (
                        <button 
                          className="uk-button uk-button-small uk-button-default uk-margin-small-right"
                          onClick={() => openEditModal(item)}
                          disabled={entityKey === 'indications'} // Показания нельзя редактировать
                        >
                          <span uk-icon="pencil"></span>
                        </button>
                      )}
                      {showButtons.delete && (
                        <button 
                          className="uk-button uk-button-small uk-button-danger"
                          onClick={() => openDeleteModal(item)}
                          disabled={entityKey === 'indications' || entityKey === 'events'} // Показания и события нельзя удалять
                        >
                          <span uk-icon="trash"></span>
                        </button>
                      )}
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
          <div className="uk-text-meta uk-text-center uk-margin-top">
            Показано записей: {data.length}
          </div>
        </div>
      )}

      {/* Модальное окно создания */}
      {showCreateModal && (
        <div className="uk-modal uk-open" style={{ display: 'block' }}>
          <div className="uk-modal-dialog">
            <button 
              className="uk-modal-close-default" 
              type="button" 
              uk-close
              onClick={() => setShowCreateModal(false)}
            ></button>
            <div className="uk-modal-header">
              <h2 className="uk-modal-title">Добавить {title.toLowerCase()}</h2>
            </div>
            <div className="uk-modal-body">
              <form>
                {getCreateFieldsConfig().map(fieldConfig => renderField(fieldConfig, false))}
              </form>
            </div>
            <div className="uk-modal-footer uk-text-right">
              <button 
                className="uk-button uk-button-default uk-modal-close" 
                type="button"
                onClick={() => setShowCreateModal(false)}
              >
                Отмена
              </button>
              <button 
                className="uk-button uk-button-primary" 
                type="button"
                onClick={handleCreate}
              >
                Создать
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Модальное окно редактирования */}
      {showEditModal && selectedItem && (
        <div className="uk-modal uk-open" style={{ display: 'block' }}>
          <div className="uk-modal-dialog">
            <button 
              className="uk-modal-close-default" 
              type="button" 
              uk-close
              onClick={() => setShowEditModal(false)}
            ></button>
            <div className="uk-modal-header">
              <h2 className="uk-modal-title">Редактировать {title.toLowerCase()}</h2>
            </div>
            <div className="uk-modal-body">
              <form>
                {getEditFieldsConfig().map(fieldConfig => renderField(fieldConfig, true))}
              </form>
            </div>
            <div className="uk-modal-footer uk-text-right">
              <button 
                className="uk-button uk-button-default uk-modal-close" 
                type="button"
                onClick={() => setShowEditModal(false)}
              >
                Отмена
              </button>
              <button 
                className="uk-button uk-button-primary" 
                type="button"
                onClick={handleUpdate}
              >
                Сохранить
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Модальное окно удаления */}
      {showDeleteModal && selectedItem && (
        <div className="uk-modal uk-open" style={{ display: 'block' }}>
          <div className="uk-modal-dialog">
            <button 
              className="uk-modal-close-default" 
              type="button" 
              uk-close
              onClick={() => setShowDeleteModal(false)}
            ></button>
            <div className="uk-modal-header">
              <h2 className="uk-modal-title">Подтверждение удаления</h2>
            </div>
            <div className="uk-modal-body">
              <p>Вы уверены, что хотите удалить этот элемент?</p>
              <div className="uk-alert-warning" uk-alert>
                <p>Это действие нельзя отменить.</p>
              </div>
            </div>
            <div className="uk-modal-footer uk-text-right">
              <button 
                className="uk-button uk-button-default uk-modal-close" 
                type="button"
                onClick={() => setShowDeleteModal(false)}
              >
                Отмена
              </button>
              <button 
                className="uk-button uk-button-danger" 
                type="button"
                onClick={handleDelete}
              >
                Удалить
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default EntitySection;