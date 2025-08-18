import React, { useState, useEffect } from 'react';
import './EmotionalForecasting.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const EmotionalForecasting = ({ user }) => {
  const [forecast, setForecast] = useState(null);
  const [forecastHistory, setForecastHistory] = useState([]);
  const [selectedPeriod, setSelectedPeriod] = useState('24h');
  const [loading, setLoading] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    loadForecast();
    loadForecastHistory();
    
    // Update current time every minute
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 60000);

    return () => clearInterval(timer);
  }, [selectedPeriod]);

  const getToken = () => localStorage.getItem('token');

  const loadForecast = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}/api/forecasting/predict?period=${selectedPeriod}`, {
        headers: {
          'Authorization': `Bearer ${getToken()}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setForecast(data);
      }
    } catch (error) {
      console.error('Failed to load forecast:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadForecastHistory = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/forecasting/history`, {
        headers: {
          'Authorization': `Bearer ${getToken()}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setForecastHistory(data.forecasts);
      }
    } catch (error) {
      console.error('Failed to load forecast history:', error);
    }
  };

  const getEmotionColor = (emotion) => {
    const colors = {
      joy: '#FFD700',
      sadness: '#4169E1',
      anger: '#FF4500',
      fear: '#800080',
      surprise: '#FF69B4',
      disgust: '#8B4513',
      trust: '#32CD32',
      anticipation: '#FFA500',
      love: '#FF1493',
      optimism: '#90EE90',
      neutral: '#4A90E2'
    };
    return colors[emotion] || '#4A90E2';
  };

  const getEmotionIcon = (emotion) => {
    const icons = {
      joy: '😊',
      sadness: '😢',
      anger: '😠',
      fear: '😨',
      surprise: '😲',
      disgust: '🤢',
      trust: '🤝',
      anticipation: '🤔',
      love: '❤️',
      optimism: '😌',
      neutral: '😐'
    };
    return icons[emotion] || '😐';
  };

  const formatTime = (timeStr) => {
    const timeMap = {
      'morning': '6:00 AM - 12:00 PM',
      'afternoon': '12:00 PM - 6:00 PM',
      'evening': '6:00 PM - 12:00 AM',
      'night': '12:00 AM - 6:00 AM'
    };
    return timeMap[timeStr] || timeStr;
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return '#32CD32'; // Green
    if (confidence >= 0.6) return '#FFA500'; // Orange
    return '#FF4500'; // Red
  };

  return (
    <div className="emotional-forecasting">
      <div className="forecasting-header">
        <h2>🔮 Emotional Forecasting</h2>
        <p>Predict your future emotional states and prepare for what's ahead</p>
      </div>

      <div className="forecasting-grid">
        {/* Forecast Controls */}
        <div className="controls-section">
          <h3>Forecast Settings</h3>
          <div className="period-selector">
            <label>Forecast Period:</label>
            <select 
              value={selectedPeriod} 
              onChange={(e) => setSelectedPeriod(e.target.value)}
              className="period-select"
            >
              <option value="24h">Next 24 Hours</option>
              <option value="7d">Next 7 Days</option>
              <option value="30d">Next 30 Days</option>
            </select>
          </div>
          
          <div className="current-time">
            <span>Current Time: {currentTime.toLocaleString()}</span>
          </div>
          
          <button 
            onClick={loadForecast}
            disabled={loading}
            className="refresh-btn"
          >
            {loading ? 'Generating Forecast...' : 'Refresh Forecast'}
          </button>
        </div>

        {/* Current Forecast */}
        {forecast && (
          <div className="forecast-section">
            <h3>Emotional Forecast</h3>
            <div className="forecast-header">
              <span className="forecast-period">{forecast.forecast_period} Forecast</span>
              <span 
                className="confidence-score"
                style={{ color: getConfidenceColor(forecast.confidence_score) }}
              >
                {(forecast.confidence_score * 100).toFixed(0)}% Confidence
              </span>
            </div>

            <div className="predicted-emotions">
              {Object.entries(forecast.predicted_emotions).map(([emotion, predictions]) => (
                <div key={emotion} className="emotion-prediction">
                  <div className="emotion-header">
                    <span className="emotion-icon">{getEmotionIcon(emotion)}</span>
                    <span className="emotion-name">{emotion}</span>
                  </div>
                  
                  <div className="time-predictions">
                    {predictions.map((prediction, index) => (
                      <div key={index} className="time-prediction">
                        <span className="time-label">{formatTime(prediction.time)}</span>
                        <div className="intensity-bar">
                          <div 
                            className="intensity-fill"
                            style={{
                              width: `${prediction.intensity * 100}%`,
                              backgroundColor: getEmotionColor(emotion)
                            }}
                          />
                        </div>
                        <span className="intensity-value">{(prediction.intensity * 100).toFixed(0)}%</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            {/* Factors Considered */}
            <div className="factors-section">
              <h4>Factors Considered</h4>
              <div className="factors-list">
                {forecast.factors_considered.map((factor, index) => (
                  <span key={index} className="factor-tag">{factor}</span>
                ))}
              </div>
            </div>

            {/* Recommendations */}
            <div className="recommendations-section">
              <h4>AI Recommendations</h4>
              <div className="recommendations-list">
                {forecast.recommendations.map((recommendation, index) => (
                  <div key={index} className="recommendation-item">
                    <span className="recommendation-icon">💡</span>
                    <span className="recommendation-text">{recommendation}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Forecast Timeline */}
        <div className="timeline-section">
          <h3>Forecast Timeline</h3>
          <div className="timeline">
            {forecast && Object.entries(forecast.predicted_emotions).map(([emotion, predictions]) => (
              <div key={emotion} className="timeline-emotion">
                <div className="timeline-emotion-header">
                  <span className="emotion-icon">{getEmotionIcon(emotion)}</span>
                  <span className="emotion-name">{emotion}</span>
                </div>
                
                <div className="timeline-predictions">
                  {predictions.map((prediction, index) => (
                    <div key={index} className="timeline-point">
                      <div className="timeline-time">{formatTime(prediction.time)}</div>
                      <div 
                        className="timeline-marker"
                        style={{
                          backgroundColor: getEmotionColor(emotion),
                          opacity: prediction.intensity
                        }}
                      />
                      <div className="timeline-intensity">{(prediction.intensity * 100).toFixed(0)}%</div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Forecast History */}
        <div className="history-section">
          <h3>Forecast History</h3>
          <div className="history-list">
            {forecastHistory.length > 0 ? (
              forecastHistory.slice(0, 5).map((historicalForecast, index) => (
                <div key={index} className="history-item">
                  <div className="history-header">
                    <span className="history-period">{historicalForecast.forecast_period}</span>
                    <span 
                      className="history-confidence"
                      style={{ color: getConfidenceColor(historicalForecast.confidence_score) }}
                    >
                      {(historicalForecast.confidence_score * 100).toFixed(0)}%
                    </span>
                  </div>
                  
                  <div className="history-emotions">
                    {Object.keys(historicalForecast.predicted_emotions).slice(0, 3).map(emotion => (
                      <span key={emotion} className="history-emotion">
                        {getEmotionIcon(emotion)} {emotion}
                      </span>
                    ))}
                  </div>
                  
                  <div className="history-date">
                    {new Date(historicalForecast.created_at).toLocaleDateString()}
                  </div>
                </div>
              ))
            ) : (
              <p className="no-history">No forecast history available yet.</p>
            )}
          </div>
        </div>

        {/* Forecast Accuracy */}
        <div className="accuracy-section">
          <h3>Forecast Accuracy</h3>
          <div className="accuracy-stats">
            <div className="accuracy-stat">
              <span className="stat-label">Short-term (24h):</span>
              <span className="stat-value">85-90%</span>
            </div>
            <div className="accuracy-stat">
              <span className="stat-label">Medium-term (7d):</span>
              <span className="stat-value">70-80%</span>
            </div>
            <div className="accuracy-stat">
              <span className="stat-label">Long-term (30d):</span>
              <span className="stat-value">60-70%</span>
            </div>
          </div>
          
          <div className="accuracy-note">
            <p>📊 Accuracy improves with more emotional data and consistent usage.</p>
          </div>
        </div>

        {/* Proactive Planning */}
        <div className="planning-section">
          <h3>Proactive Planning</h3>
          <div className="planning-tips">
            <div className="planning-tip">
              <h4>🎯 High Confidence Forecasts</h4>
              <p>Use high-confidence predictions to plan activities and prepare emotionally.</p>
            </div>
            <div className="planning-tip">
              <h4>⚠️ Low Confidence Forecasts</h4>
              <p>When confidence is low, focus on building emotional resilience and flexibility.</p>
            </div>
            <div className="planning-tip">
              <h4>📈 Trend Analysis</h4>
              <p>Look for patterns in your emotional forecasts to understand your cycles.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EmotionalForecasting; 