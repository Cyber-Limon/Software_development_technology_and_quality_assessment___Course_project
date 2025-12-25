import React from 'react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, 
  Tooltip, ResponsiveContainer, ReferenceLine
} from 'recharts';

const IndicationChart = ({ 
  data, 
  sensorType = 'Датчик', 
  sensorId = '', 
  minLimit, 
  maxLimit 
}) => {
  // Форматируем данные для графика
  const chartData = data.map(item => ({
    time: new Date(item.time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    fullTime: new Date(item.time).toLocaleString(),
    value: parseFloat(item.value.toFixed(2)),
    status: item.status,
    // Цвет в зависимости от статуса
    color: item.status === 'Нормальное' ? '#10b981' : 
           item.status === 'Возможно превышение' ? '#f59e0b' : 
           '#ef4444'
  }));

  // Находим min и max значений для масштабирования графика
  const values = chartData.map(d => d.value);
  const dataMin = Math.min(...values);
  const dataMax = Math.max(...values);
  
  // Вычисляем границы для оси Y
  const yMin = Math.min(dataMin - 5, minLimit ? minLimit - 5 : dataMin - 5);
  const yMax = Math.max(dataMax + 5, maxLimit ? maxLimit + 5 : dataMax + 5);

  // Кастомная точка для графика
  const CustomDot = (props) => {
    const { cx, cy, payload } = props;
    return (
      <circle 
        cx={cx} 
        cy={cy} 
        r={4} 
        fill={payload.color}
        stroke="#fff"
        strokeWidth={2}
      />
    );
  };

  return (
    <div className="uk-card uk-card-default uk-card-body">
      <h4 className="uk-card-title uk-text-center">
        График показаний: {sensorType}
        {sensorId && ` (ID датчика: ${sensorId})`}
      </h4>
      
      <div style={{ width: '100%', height: 350 }}>
        <ResponsiveContainer>
          <LineChart
            data={chartData}
            margin={{ top: 10, right: 30, left: 20, bottom: 10 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis 
              dataKey="time" 
              tick={{ fontSize: 11 }}
              label={{ value: 'Время', position: 'insideBottom', offset: -5 }}
            />
            <YAxis 
              domain={[yMin, yMax]}
              label={{ value: 'Значение', angle: -90, position: 'insideLeft' }}
            />
            
            {/* Линия минимума (если есть) */}
            {minLimit !== undefined && minLimit !== null && (
              <ReferenceLine 
                y={minLimit} 
                stroke="#ef4444" 
                strokeDasharray="5 5"
                strokeWidth={1.5}
                label={{ 
                  value: `Мин: ${minLimit}`, 
                  position: 'right',
                  fill: '#ef4444',
                  fontSize: 11,
                  offset: 5
                }}
              />
            )}
            
            {/* Линия максимума (если есть) */}
            {maxLimit !== undefined && maxLimit !== null && (
              <ReferenceLine 
                y={maxLimit} 
                stroke="#ef4444" 
                strokeDasharray="5 5"
                strokeWidth={1.5}
                label={{ 
                  value: `Макс: ${maxLimit}`, 
                  position: 'right',
                  fill: '#ef4444',
                  fontSize: 11,
                  offset: 5
                }}
              />
            )}
            
            <Tooltip 
              formatter={(value, name, props) => {
                if (name === 'value') {
                  return [
                    <span style={{ color: '#3b82f6', fontWeight: 'bold' }}>
                      {value}
                    </span>, 
                    'Значение'
                  ];
                }
                const statusColor = props.payload.status === 'Нормальное' ? '#10b981' : 
                                   props.payload.status === 'Возможно превышение' ? '#f59e0b' : 
                                   '#ef4444';
                return [
                  <span style={{ color: statusColor, fontWeight: 'bold' }}>
                    {props.payload.status}
                  </span>, 
                  'Статус'
                ];
              }}
              labelFormatter={(label, items) => {
                const item = items?.[0]?.payload;
                return item ? `Время: ${item.fullTime}` : `Время: ${label}`;
              }}
              contentStyle={{ 
                backgroundColor: 'white', 
                border: '1px solid #ccc',
                borderRadius: '5px',
                padding: '10px'
              }}
            />
            
            {/* Основная линия графика */}
            <Line
              type="monotone"
              dataKey="value"
              stroke="#3b82f6"
              strokeWidth={2}
              dot={<CustomDot />}
              activeDot={{ 
                r: 6, 
                strokeWidth: 2,
                fill: '#3b82f6',
                stroke: '#fff'
              }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
      
      {/* Единая легенда */}
      <div className="uk-flex uk-flex-center uk-flex-wrap uk-margin-top">
        {/* Линия показаний */}
        <div className="uk-flex uk-flex-middle uk-margin-small-right">
          <div className="uk-margin-small-right" style={{ 
            width: '20px', 
            height: '3px', 
            backgroundColor: '#3b82f6',
            marginTop: '1px'
          }}></div>
          <span className="uk-text-small">Показания</span>
        </div>
        
        {/* Статусы */}
        <div className="uk-flex uk-flex-middle uk-margin-small-right">
          <svg width="16" height="16" className="uk-margin-small-right">
            <circle cx="8" cy="8" r="5" fill="#10b981" stroke="#fff" strokeWidth="1" />
          </svg>
          <span className="uk-text-small">Нормальное</span>
        </div>
        <div className="uk-flex uk-flex-middle uk-margin-small-right">
          <svg width="16" height="16" className="uk-margin-small-right">
            <circle cx="8" cy="8" r="5" fill="#f59e0b" stroke="#fff" strokeWidth="1" />
          </svg>
          <span className="uk-text-small">Возможно превышение</span>
        </div>
        <div className="uk-flex uk-flex-middle uk-margin-small-right">
          <svg width="16" height="16" className="uk-margin-small-right">
            <circle cx="8" cy="8" r="5" fill="#ef4444" stroke="#fff" strokeWidth="1" />
          </svg>
          <span className="uk-text-small">Превышенное</span>
        </div>
        
        {/* Границы нормы */}
        {(minLimit !== undefined || maxLimit !== undefined) && (
          <div className="uk-flex uk-flex-middle uk-margin-small-right">
            <span className="uk-margin-small-right" style={{ 
              borderTop: '2px dashed #ef4444', 
              width: '20px',
              display: 'inline-block',
              marginTop: '1px'
            }}></span>
            <span className="uk-text-small">Границы нормы</span>
          </div>
        )}
      </div>
      
      {/* Статистика */}
      {chartData.length > 0 && (
        <div className="uk-grid uk-grid-small uk-margin-top" data-uk-grid>
          <div className="uk-width-1-4">
            <div className="uk-card uk-card-small uk-card-secondary uk-card-body">
              <p className="uk-text-small uk-margin-remove">Всего записей</p>
              <p className="uk-text-lead uk-margin-remove">{chartData.length}</p>
            </div>
          </div>
          <div className="uk-width-1-4">
            <div className="uk-card uk-card-small uk-card-secondary uk-card-body">
              <p className="uk-text-small uk-margin-remove">Среднее</p>
              <p className="uk-text-lead uk-margin-remove">
                {(chartData.reduce((sum, item) => sum + item.value, 0) / chartData.length).toFixed(2)}
              </p>
            </div>
          </div>
          <div className="uk-width-1-4">
            <div className="uk-card uk-card-small uk-card-secondary uk-card-body">
              <p className="uk-text-small uk-margin-remove">Минимум</p>
              <p className="uk-text-lead uk-margin-remove">
                {dataMin.toFixed(2)}
              </p>
            </div>
          </div>
          <div className="uk-width-1-4">
            <div className="uk-card uk-card-small uk-card-secondary uk-card-body">
              <p className="uk-text-small uk-margin-remove">Максимум</p>
              <p className="uk-text-lead uk-margin-remove">
                {dataMax.toFixed(2)}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default IndicationChart;