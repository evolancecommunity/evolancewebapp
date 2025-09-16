import React, { useState, useEffect, useRef } from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Brush
} from 'recharts';
import InteractiveAvatar, { EvIcon, EvBubble } from './InteractiveAvatar';
import avatar from '../assets/avatar.png';
import '../EmolyticsAnimations.css';

const emotionColors = {
  Joy: '#facc15',
  Sadness: '#3b82f6',
  Anger: '#ef4444',
  Fear: '#a21caf',
  Surprise: '#06b6d4',
  Disgust: '#22c55e',
};

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const Emolytics = ({ user }) => {
  const [textInput, setTextInput] = useState('');
  const [emotionAnalysis, setEmotionAnalysis] = useState(null);
  const [emotionalProfile, setEmotionalProfile] = useState(null);
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const [emotionData, setEmotionData] = useState({});
  const [loadingEmolytics, setLoadingEmolytics] = useState(true);
  const [errorEmolytics, setErrorEmolytics] = useState(null);

  useEffect(() => {
    loadEmotionalProfile();
    loadInsights();
    const token = localStorage.getItem('token');
    fetch(`${BACKEND_URL}/api/ai/emotional-state/timeseries`, {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch emolytics');
        return res.json();
      })
      .then(data => {
        setEmotionData(data.emotions || data); // adjust if backend wraps in {emotions: ...}
        setLoadingEmolytics(false);
      })
      .catch(err => {
        setErrorEmolytics(err.message);
        setLoadingEmolytics(false);
      });
  }, []);

  const getToken = () => localStorage.getItem('token');

  const loadEmotionalProfile = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/emolytics/profile`, {
        headers: {
          'Authorization': `Bearer ${getToken()}`
        }
      });
      
      if (response.ok) {
        const profile = await response.json();
        setEmotionalProfile(profile);
      }
    } catch (error) {
      console.error('Failed to load emotional profile:', error);
    }
  };

  const loadInsights = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/emolytics/insights`, {
        headers: {
          'Authorization': `Bearer ${getToken()}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setInsights(data.insights);
      }
    } catch (error) {
      console.error('Failed to load insights:', error);
    }
  };

  const analyzeEmotions = async () => {
    if (!textInput.trim()) return;

    setLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}/api/emolytics/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${getToken()}`
        },
        body: JSON.stringify({
          text: textInput,
          context: 'user_input'
        })
      });

      if (response.ok) {
        const analysis = await response.json();
        setEmotionAnalysis(analysis);
        
        // Add to chat history
        setChatHistory(prev => [...prev, {
          text: textInput,
          emotions: analysis.emotions,
          primary_emotion: analysis.primary_emotion,
          timestamp: new Date()
        }]);
        
        setTextInput('');
        
        // Reload profile and insights
        loadEmotionalProfile();
        loadInsights();
      }
    } catch (error) {
      console.error('Failed to analyze emotions:', error);
    } finally {
      setLoading(false);
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
      optimism: '#90EE90'
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
      optimism: '😌'
    };
    return icons[emotion] || '😐';
  };

  if (loadingEmolytics) return <div className="text-white text-center py-12">Loading your emolytics...</div>;
  if (errorEmolytics) return <div className="text-red-400 text-center py-12">Error: {errorEmolytics}</div>;
  if (!emotionData || Object.keys(emotionData).length === 0) return <div className="text-white text-center py-12">No emolytics data yet.</div>;

  return (
    <div className="emolytics">
      <div className="emolytics-header">
        <h2>🧠 Emolytics Dashboard</h2>
        <p>Analyze your emotions and discover patterns in your emotional intelligence</p>
      </div>

      <div className="emolytics-grid">
        {/* Emotion Analysis Input */}
        <div className="analysis-section">
          <h3>Analyze Your Emotions</h3>
          <div className="input-group">
            <textarea
              value={textInput}
              onChange={(e) => setTextInput(e.target.value)}
              placeholder="Describe how you're feeling or what's on your mind..."
              className="emotion-input"
              rows="4"
            />
            <button 
              onClick={analyzeEmotions}
              disabled={loading || !textInput.trim()}
              className="analyze-btn"
            >
              {loading ? 'Analyzing...' : 'Analyze Emotions'}
            </button>
          </div>
        </div>

        {/* Current Analysis Results */}
        {emotionAnalysis && (
          <div className="analysis-results">
            <h3>Emotion Analysis Results</h3>
            <div className="emotion-breakdown">
              <div className="primary-emotion">
                <span className="emotion-icon">{getEmotionIcon(emotionAnalysis.primary_emotion)}</span>
                <span className="emotion-name">{emotionAnalysis.primary_emotion}</span>
                <span className="emotion-intensity">{(emotionAnalysis.intensity * 100).toFixed(0)}%</span>
              </div>
              
              <div className="emotion-chart">
                {Object.entries(emotionAnalysis.emotions).map(([emotion, intensity]) => (
                  <div key={emotion} className="emotion-bar">
                    <span className="emotion-label">{emotion}</span>
                    <div className="bar-container">
                      <div 
                        className="bar-fill"
                        style={{
                          width: `${intensity * 100}%`,
                          backgroundColor: getEmotionColor(emotion)
                        }}
                      />
                    </div>
                    <span className="intensity-value">{(intensity * 100).toFixed(0)}%</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Emotional Profile */}
        {emotionalProfile && (
          <div className="profile-section">
            <h3>Your Emotional Profile</h3>
            <div className="profile-stats">
              <div className="stat-card">
                <h4>Total Interactions</h4>
                <span className="stat-value">{emotionalProfile.total_interactions}</span>
              </div>
              <div className="stat-card">
                <h4>Dominant Emotion</h4>
                <span className="stat-value">{emotionalProfile.dominant_emotion}</span>
              </div>
              <div className="stat-card">
                <h4>Emotional Stability</h4>
                <span className="stat-value">{(emotionalProfile.emotional_stability_score * 100).toFixed(0)}%</span>
              </div>
            </div>
            
            <div className="emotional-fingerprint">
              <h4>Emotional Fingerprint</h4>
              <div className="fingerprint-chart">
                {Object.entries(emotionalProfile.emotional_fingerprint).map(([emotion, intensity]) => (
                  <div key={emotion} className="fingerprint-item">
                    <span className="emotion-icon">{getEmotionIcon(emotion)}</span>
                    <span className="emotion-name">{emotion}</span>
                    <div className="fingerprint-bar">
                      <div 
                        className="fingerprint-fill"
                        style={{
                          width: `${intensity * 100}%`,
                          backgroundColor: getEmotionColor(emotion)
                        }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* AI Insights */}
        <div className="insights-section">
          <h3>AI-Generated Insights</h3>
          {insights.length > 0 ? (
            <div className="insights-list">
              {insights.map((insight, index) => (
                <div key={index} className="insight-card">
                  <div className="insight-header">
                    <span className="insight-type">{insight.type}</span>
                    <span className="confidence">{(insight.confidence * 100).toFixed(0)}% confidence</span>
                  </div>
                  <h4>{insight.title}</h4>
                  <p>{insight.description}</p>
                </div>
              ))}
            </div>
          ) : (
            <p className="no-insights">Start analyzing your emotions to get personalized insights!</p>
          )}
        </div>

        {/* Recent Chat History */}
        <div className="chat-history-section">
          <h3>Recent Emotional Analysis</h3>
          <div className="chat-history">
            {chatHistory.slice(-5).reverse().map((entry, index) => (
              <div key={index} className="chat-entry">
                <div className="entry-text">{entry.text}</div>
                <div className="entry-emotions">
                  <span className="primary-emotion">
                    {getEmotionIcon(entry.primary_emotion)} {entry.primary_emotion}
                  </span>
                  <span className="timestamp">
                    {entry.timestamp.toLocaleTimeString()}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Emolytics; 