// Функция для входа в систему
export const login = async (username, password) => {
  try {
    // Кодируем логин и пароль в Base64 для Basic Auth
    const credentials = btoa(`${username}:${password}`);
    
    // Сохраняем в localStorage для использования в interceptor
    localStorage.setItem('credentials', credentials);
    
    // Тестовый запрос для проверки валидности учетных данных
    const response = await fetch('http://127.0.0.1:8000/api/company', {
      method: 'GET',
      headers: {
        'Authorization': `Basic ${credentials}`,
        'Accept': 'application/json'
      }
    });
    
    if (!response.ok) {
      localStorage.removeItem('credentials');
      throw new Error('Неверный логин или пароль');
    }
    
    return { success: true };
  } catch (error) {
    localStorage.removeItem('credentials');
    throw error;
  }
};

// Функция для выхода
export const logout = () => {
  localStorage.removeItem('credentials');
};

// Проверка авторизации
export const isAuthenticated = () => {
  return !!localStorage.getItem('credentials');
};

// Получение текущих учетных данных
export const getCredentials = () => {
  return localStorage.getItem('credentials');
};