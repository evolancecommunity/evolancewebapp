import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../App';
import './Dashboard.css';
import ReactApexChart from 'react-apexcharts';
import AvatarVisualization from './AvatarVisualization';

const Dashboard = () => {
  const [user, setUser] = useState(null);
  const [emotionalState, setEmotionalState] = useState(null);
  const [avatarData, setAvatarData] = useState(null);
  const [consciousnessJourney, setConsciousnessJourney] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [decisionText, setDecisionText] = useState('');
  const [visualization, setVisualization] = useState(null);
  const [visualizing, setVisualizing] = useState(false);
  const [visualizationError, setVisualizationError] = useState(null);
  const navigate = useNavigate();
  const { API } = useContext(AuthContext);

  useEffect(() => {
    fetchUserData();
    fetchEmotionalState();
    fetchAvatarData();
    fetchConsciousnessJourney();
  }, [API]);

  const fetchUserData = async () => {
    try {
      const token = localStorage.getItem('token');
      if (token) {
        const response = await axios.get(`${API}/auth/me`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setUser(response.data);
      }
    } catch (error) {
      console.error('Error fetching user data:', error);
    }
  };

  const fetchEmotionalState = async () => {
    try {
      const token = localStorage.getItem('token');
      if (token) {
        const response = await axios.get(`${API}/ai/emotional-state/timeseries`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setEmotionalState(response.data);
      }
    } catch (error) {
      console.error('Error fetching emotional state:', error);
    }
  };

  const fetchAvatarData = async () => {
    try {
      const token = localStorage.getItem('token');
      if (token) {
        const response = await axios.get(`${API}/ai/avatar`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setAvatarData(response.data);
      }
    } catch (error) {
      console.error('Error fetching avatar data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchConsciousnessJourney = async () => {
    try {
      const token = localStorage.getItem('token');
      if (token) {
        const response = await axios.get(`${API}/consciousness/journey`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setConsciousnessJourney(response.data);
      }
    } catch (error) {
      console.error('Error fetching consciousness journey:', error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  const handleVisualizeDecision = async () => {
    setVisualizing(true);
    setVisualizationError(null);
    setVisualization(null);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        `${API}/ai/visualize-decision`,
        { decision: decisionText },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setVisualization(response.data);
    } catch (error) {
      setVisualizationError('Could not visualize decision.');
    } finally {
      setVisualizing(false);
    }
  };

  if (isLoading) {
    return (
      <div className="dashboard-loading">
        <div className="loading-spinner"></div>
        <p className="loading-text">Initializing your consciousness journey...</p>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <div className="logo-section">
            <h1 className="app-title">Evolance</h1>
            <p className="app-subtitle">Emotional Wellbeing AI</p>
          </div>
          <div className="header-actions">
            <button
              className="header-action-btn chat-btn"
              onClick={() => navigate('/chat')}
            >
              <span className="btn-icon">💬</span>
              <span className="btn-text">Talk about it!</span>
            </button>
            <button
              className="header-action-btn profile-btn"
              onClick={() => navigate('/profile')}
              title="View Profile"
            >
              <span className="btn-icon">👤</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="dashboard-main">
        <div className="dashboard-grid">
          {/* Welcome Section */}
          <section className="welcome-section">
            <div className="welcome-content">
              <h2 className="welcome-title">
                Welcome back, {user?.full_name?.split(' ')[0] || user?.username || 'there'}
              </h2>
              <p className="welcome-message">
                How are you feeling today? I'm here to support your emotional wellbeing.
              </p>
            </div>
          </section>

          {/* Visualize a Decision Card */}
          <section className="journey-card">
            <div className="card-header">
              <h3 className="card-title">Visualize a Decision</h3>
              <p className="card-subtitle">See how your choices might shape your emotional journey</p>
            </div>
            <div className="card-content">
              <div className="decision-input-wrapper">
                <textarea
                  className="decision-input"
                  placeholder=" "
                  value={decisionText}
                  onChange={e => setDecisionText(e.target.value)}
                  rows={3}
                  id="decision-input"
                />
                <label htmlFor="decision-input" className="decision-label">
                  Describe a decision you're considering...
                </label>
              </div>
              <button
                className="explore-btn"
                onClick={handleVisualizeDecision}
                disabled={visualizing || !decisionText.trim()}
                style={{ marginBottom: 12 }}
              >
                {visualizing ? 'Visualizing...' : 'Visualize Emotional Impact'}
              </button>
              {visualizationError && (
                <div className="error-message">{visualizationError}</div>
              )}
              {visualization && (
                <div className="visualization-results">
                  <div className="viz-row">
                    <strong>Past:</strong> {visualization.past?.emotion || 'N/A'}
                    <span style={{ marginLeft: 8, color: '#888' }}>{visualization.past?.description}</span>
                  </div>
                  <div className="viz-row">
                    <strong>Present:</strong> {visualization.present?.emotion || 'N/A'}
                    <span style={{ marginLeft: 8, color: '#888' }}>{visualization.present?.description}</span>
                  </div>
                  <div className="viz-row">
                    <strong>Future:</strong> {visualization.future?.emotion || 'N/A'}
                    <span style={{ marginLeft: 8, color: '#888' }}>{visualization.future?.description}</span>
                  </div>
                </div>
              )}
            </div>
          </section>

          {/* Emotional Profile Card */}
          <section className="emotional-card">
            <div className="card-header">
              <h3 className="card-title">Emotional Intelligence</h3>
              <p className="card-subtitle">Your current emotional landscape</p>
            </div>
            <div className="card-content">
              {emotionalState && emotionalState.emotions ? (
                <div className="emotional-metrics">
                  {Object.entries(emotionalState.emotions).slice(0, 3).map(([emotionName, timeSeries]) => {
                    const latestValue = timeSeries[timeSeries.length - 1]?.value || 0;
                    const emotionColors = {
                      joy: '#FFD700',
                      sadness: '#4169E1',
                      anger: '#DC143C',
                      fear: '#9932CC',
                      surprise: '#00CED1',
                      disgust: '#32CD32',
                      trust: '#FF69B4',
                      anticipation: '#FF8C00'
                    };
                    const color = emotionColors[emotionName] || '#808080';
                    
                    return (
                      <div key={emotionName} className="metric">
                        <span className="metric-label" style={{ color }}>
                          {emotionName.charAt(0).toUpperCase() + emotionName.slice(1)}
                        </span>
                        <span className="metric-value">{Math.round(latestValue)}%</span>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <div className="placeholder-content">
                  <p>Emotional data will appear here</p>
                </div>
              )}
            </div>
          </section>

          {/* Avatar Visualization Card */}
          <section className="avatar-card">
            <div className="card-header">
              <h3 className="card-title">Emotional Avatar</h3>
              <p className="card-subtitle">Visual representation of your emotional state</p>
            </div>
            <div className="card-content">
              <div className="avatar-preview">
                <AvatarVisualization 
                  size="large" 
                  showDetails={false} 
                  className="mx-auto"
                />
              </div>
            </div>
          </section>

          {/* Interactive Emotion Graphs */}
          <section className="graphs-card">
            <div className="card-header">
              <h3 className="card-title">Emolytics</h3>
              <p className="card-subtitle">Your Emotional Analytics</p>
            </div>
            <div className="card-content">
              <div className="graphs-container">
                {emotionalState && emotionalState.emotions ? (
                  Object.entries(emotionalState.emotions).map(([emotionName, timeSeries]) => {
                    const emotionColors = {
                      joy: { color: '#FFD700', gradient: ['#FFD700', '#FFA500'] },
                      sadness: { color: '#4169E1', gradient: ['#4169E1', '#1E40AF'] },
                      anger: { color: '#DC143C', gradient: ['#DC143C', '#B91C1C'] },
                      fear: { color: '#9932CC', gradient: ['#9932CC', '#7C3AED'] },
                      surprise: { color: '#00CED1', gradient: ['#00CED1', '#06B6D4'] },
                      disgust: { color: '#32CD32', gradient: ['#32CD32', '#059669'] },
                      trust: { color: '#FF69B4', gradient: ['#FF69B4', '#EC4899'] },
                      anticipation: { color: '#FF8C00', gradient: ['#FF8C00', '#EA580C'] }
                    };
                    
                    const colors = emotionColors[emotionName] || { color: '#808080', gradient: ['#808080', '#6B7280'] };
                    
                    const series = [{
                      name: emotionName.charAt(0).toUpperCase() + emotionName.slice(1),
                      data: timeSeries.map(point => point.value)
                    }];
                    
                    const categories = timeSeries.map(point => {
                      const date = new Date(point.timestamp);
                      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
                    });
                    
                    const options = {
                      chart: {
                        type: 'area',
                        height: 250,
                        toolbar: { show: false },
                        background: 'transparent',
                      },
                      theme: { mode: 'dark' },
                      dataLabels: { enabled: false },
                      stroke: {
                        curve: 'smooth',
                        width: 2,
                        colors: [colors.gradient[0]]
                      },
                      fill: {
                        type: 'gradient',
                        gradient: {
                          shade: 'dark',
                          type: 'vertical',
                          shadeIntensity: 0.5,
                          gradientToColors: [colors.gradient[1]],
                          inverseColors: false,
                          opacityFrom: 0.7,
                          opacityTo: 0.1,
                          stops: [0, 100]
                        }
                      },
                      xaxis: {
                        categories: categories,
                        labels: {
                          style: { colors: '#b0b8d1', fontSize: '12px' }
                        },
                        axisBorder: { show: false },
                        axisTicks: { show: false },
                      },
                      yaxis: {
                        show: false
                      },
                      grid: {
                        show: false
                      },
                      tooltip: {
                        theme: 'dark',
                        y: {
                          formatter: (val) => `${val}%`
                        }
                      },
                      colors: [colors.gradient[0]],
                      legend: { show: false },
                    };
                    
                    return (
                      <div key={emotionName} className="emotion-graph">
                        <div className="graph-header">
                          <span className="emotion-name">{emotionName.charAt(0).toUpperCase() + emotionName.slice(1)}</span>
                        </div>
                        <ReactApexChart options={options} series={series} type="area" height={250} />
                      </div>
                    );
                  })
                ) : (
                  <div className="placeholder-content">
                    <p>Loading emotional analytics...</p>
                  </div>
                )}
              </div>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
