import axios from 'axios';

// Базовый URL вашего FastAPI-сервера
const API_BASE_URL = 'http://127.0.0.1:8000';

// Создаем экземпляр axios с базовыми настройками
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  }
});

// Перехватчик для добавления Basic Auth к каждому запросу
api.interceptors.request.use(
  (config) => {
    const credentials = localStorage.getItem('credentials');
    if (credentials) {
      config.headers.Authorization = `Basic ${credentials}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Перехватчик для обработки ошибок с извлечением детальных сообщений
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response) {
      // Извлекаем детальное сообщение из FastAPI
      const detail = error.response.data?.detail;
      let errorMessage;
      
      if (detail) {
        // Если detail - массив
        if (Array.isArray(detail)) {
          errorMessage = detail.map(err => err.msg || JSON.stringify(err)).join(', ');
        }
        // Если detail - строка (ваши кастомные ошибки)
        else if (typeof detail === 'string') {
          errorMessage = detail;
        }
        // Если detail - объект
        else {
          errorMessage = JSON.stringify(detail);
        }
      } else {
        // Если нет detail, используем стандартное сообщение
        errorMessage = `HTTP ${error.response.status}: ${error.response.statusText}`;
      }
      
      // Создаем новую ошибку с правильным сообщением
      const customError = new Error(errorMessage);
      customError.status = error.response.status;
      customError.response = error.response;
      
      // Обработка 401 ошибки (неавторизован)
      if (error.response.status === 401) {
        localStorage.removeItem('credentials');
        window.location.href = '/login';
      }
      
      return Promise.reject(customError);
    }
    
    // Если нет response (сетевая ошибка)
    return Promise.reject(error);
  }
);

export default api;