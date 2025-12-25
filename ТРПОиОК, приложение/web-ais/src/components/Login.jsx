import React, { useState } from 'react';
import { login } from '../services/auth';

const Login = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await login(username, password);
      onLoginSuccess();
    } catch (err) {
      setError(err.message || 'Ошибка авторизации');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="uk-height-1-1 uk-flex uk-flex-middle uk-flex-center">
      <div className="uk-width-medium uk-card uk-card-default uk-card-body">
        <h2 className="uk-card-title uk-text-center">Вход в систему "АС-СКУД"</h2>
        
        {error && (
          <div className="uk-alert-danger uk-margin" uk-alert>
            <p>{error}</p>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="uk-margin">
            <label className="uk-form-label">Логин</label>
            <div className="uk-form-controls">
              <input
                className="uk-input"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                disabled={loading}
                placeholder="Введите логин"
              />
            </div>
          </div>

          <div className="uk-margin">
            <label className="uk-form-label">Пароль</label>
            <div className="uk-form-controls">
              <input
                className="uk-input"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                disabled={loading}
                placeholder="Введите пароль"
              />
            </div>
          </div>

          <div className="uk-margin">
            <button
              className="uk-button uk-button-primary uk-width-1-1"
              type="submit"
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="uk-margin-small-right" uk-spinner="ratio: 0.5"></span>
                  Вход...
                </>
              ) : (
                'Войти'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;