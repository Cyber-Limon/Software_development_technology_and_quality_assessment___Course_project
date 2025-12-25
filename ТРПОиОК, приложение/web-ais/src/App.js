import React, { useState, useEffect } from 'react';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import { isAuthenticated } from './services/auth';

function App() {
  const [authenticated, setAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  // Проверяем авторизацию при загрузке приложения
  useEffect(() => {
    const checkAuth = () => {
      const auth = isAuthenticated();
      setAuthenticated(auth);
      setLoading(false);
    };
    
    checkAuth();
  }, []);

  // Обработчик успешного входа
  const handleLoginSuccess = () => {
    setAuthenticated(true);
  };

  // Обработчик выхода
  const handleLogout = () => {
    localStorage.removeItem('credentials');
    setAuthenticated(false);
  };

  if (loading) {
    return (
      <div className="uk-height-1-1 uk-flex uk-flex-middle uk-flex-center">
        <div className="uk-text-center">
          <span uk-spinner="ratio: 2"></span>
          <p className="uk-margin-small-top">Загрузка...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      {!authenticated ? (
        <Login onLoginSuccess={handleLoginSuccess} />
      ) : (
        <>
          {/* Шапка с кнопкой выхода */}
          <nav className="uk-navbar-container uk-navbar-transparent" uk-navbar>
            <div className="uk-navbar-left">
              <div className="uk-navbar-item">
                <h3 className="uk-margin-remove">Система контроля и управления датчиками</h3>
              </div>
            </div>
            <div className="uk-navbar-right">
              <div className="uk-navbar-item">
                <button 
                  className="uk-button uk-button-danger uk-button-small"
                  onClick={handleLogout}
                >
                  <span uk-icon="sign-out"></span> Выйти
                </button>
              </div>
            </div>
          </nav>

          {/* Основной контент */}
          <Dashboard />
        </>
      )}
    </div>
  );
}

export default App;