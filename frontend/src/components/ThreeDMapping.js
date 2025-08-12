import React, { useState, useEffect } from 'react';
import './ThreeDMapping.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const ThreeDMapping = ({ user }) => {
  const [textInput, setTextInput] = useState('');
  const [landscape, setLandscape] = useState(null);
  const [avatar, setAvatar] = useState(null);
  const [loading, setLoading] = useState(false);
  const [currentPosition, setCurrentPosition] = useState(null);

  useEffect(() => {
    loadLandscape();
    loadAvatar();
  }, []);

  const getToken = () => localStorage.getItem('token');

  const loadLandscape = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/3d-mapping/landscape`, {
        headers: {
          'Authorization': `Bearer ${getToken()}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setLandscape(data);
        setCurrentPosition(data.current_position);
      }
    } catch (error) {
      console.error('Failed to load landscape:', error);
    }
  };

  const loadAvatar = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/3d-mapping/avatar`, {
        headers: {
          'Authorization': `Bearer ${getToken()}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setAvatar(data);
      }
    } catch (error) {
      console.error('Failed to load avatar:', error);
    }
  };

  const updatePosition = async () => {
    if (!textInput.trim()) return;

    setLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}/api/3d-mapping/update-position`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${getToken()}`
        },
        body: JSON.stringify({
          text: textInput
        })
      });

      if (response.ok) {
        const data = await response.json();
        setCurrentPosition(data.position);
        setTextInput('');
        
        // Reload landscape and avatar
        loadLandscape();
        loadAvatar();
      }
    } catch (error) {
      console.error('Failed to update position:', error);
    } finally {
      setLoading(false);
    }
  };

  const getValenceLabel = (x) => {
    if (x > 0.5) return 'Very Positive';
    if (x > 0) return 'Positive';
    if (x > -0.5) return 'Neutral';
    return 'Negative';
  };

  const getArousalLabel = (y) => {
    if (y > 0.5) return 'Very Excited';
    if (y > 0) return 'Excited';
    if (y > -0.5) return 'Calm';
    return 'Very Calm';
  };

  const getDominanceLabel = (z) => {
    if (z > 0.5) return 'Very Dominant';
    if (z > 0) return 'Dominant';
    if (z > -0.5) return 'Neutral';
    return 'Submissive';
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

  return (
    <div className="three-d-mapping">
      <div className="mapping-header">
        <h2>🗺️ 3D Emotional Mapping</h2>
        <p>Explore your emotional landscape in three-dimensional space</p>
      </div>

      <div className="mapping-grid">
        {/* Input Section */}
        <div className="input-section">
          <h3>Update Your Emotional Position</h3>
          <div className="input-group">
            <textarea
              value={textInput}
              onChange={(e) => setTextInput(e.target.value)}
              placeholder="Describe your current emotional state..."
              className="emotion-input"
              rows="4"
            />
            <button 
              onClick={updatePosition}
              disabled={loading || !textInput.trim()}
              className="update-btn"
            >
              {loading ? 'Updating...' : 'Update Position'}
            </button>
          </div>
        </div>

        {/* Current Position Display */}
        {currentPosition && (
          <div className="position-section">
            <h3>Current Emotional Position</h3>
            <div className="position-display">
              <div className="coordinate">
                <span className="coordinate-label">Valence (X):</span>
                <span className="coordinate-value">{currentPosition.x.toFixed(2)}</span>
                <span className="coordinate-description">{getValenceLabel(currentPosition.x)}</span>
              </div>
              <div className="coordinate">
                <span className="coordinate-label">Arousal (Y):</span>
                <span className="coordinate-value">{currentPosition.y.toFixed(2)}</span>
                <span className="coordinate-description">{getArousalLabel(currentPosition.y)}</span>
              </div>
              <div className="coordinate">
                <span className="coordinate-label">Dominance (Z):</span>
                <span className="coordinate-value">{currentPosition.z.toFixed(2)}</span>
                <span className="coordinate-description">{getDominanceLabel(currentPosition.z)}</span>
              </div>
              <div className="emotion-info">
                <span className="emotion-label">Primary Emotion:</span>
                <span 
                  className="emotion-value"
                  style={{ color: getEmotionColor(currentPosition.emotion) }}
                >
                  {currentPosition.emotion}
                </span>
                <span className="intensity">{(currentPosition.intensity * 100).toFixed(0)}% intensity</span>
              </div>
            </div>
          </div>
        )}

        {/* 3D Visualization */}
        <div className="visualization-section">
          <h3>3D Emotional Space</h3>
          <div className="three-d-canvas">
            <div className="canvas-container">
              <div className="axis-labels">
                <div className="x-axis">Valence (Positive ↔ Negative)</div>
                <div className="y-axis">Arousal (Calm ↔ Excited)</div>
                <div className="z-axis">Dominance (Submissive ↔ Dominant)</div>
              </div>
              
              <div className="emotional-space">
                {/* Current Position Marker */}
                {currentPosition && (
                  <div 
                    className="position-marker"
                    style={{
                      left: `${((currentPosition.x + 1) / 2) * 100}%`,
                      top: `${((currentPosition.y + 1) / 2) * 100}%`,
                      backgroundColor: getEmotionColor(currentPosition.emotion),
                      transform: `translateZ(${currentPosition.z * 50}px)`
                    }}
                    title={`${currentPosition.emotion} (${(currentPosition.intensity * 100).toFixed(0)}%)`}
                  />
                )}
                
                {/* Historical Path */}
                {landscape?.emotional_path && (
                  <div className="emotional-path">
                    {landscape.emotional_path.slice(-20).map((point, index) => (
                      <div
                        key={index}
                        className="path-point"
                        style={{
                          left: `${((point.x + 1) / 2) * 100}%`,
                          top: `${((point.y + 1) / 2) * 100}%`,
                          backgroundColor: getEmotionColor(point.emotion),
                          opacity: (index + 1) / landscape.emotional_path.slice(-20).length,
                          transform: `translateZ(${point.z * 50}px)`
                        }}
                      />
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Avatar State */}
        {avatar && (
          <div className="avatar-section">
            <h3>Your Emotional Avatar</h3>
            <div className="avatar-display">
              <div 
                className="avatar-visual"
                style={{
                  backgroundColor: avatar.primary_color,
                  borderColor: avatar.secondary_color,
                  transform: `scale(${avatar.size})`,
                  boxShadow: `0 0 ${avatar.glow_intensity * 20}px ${avatar.primary_color}`
                }}
              >
                <div className="avatar-face">
                  <div className="avatar-eyes">
                    <div className="eye left"></div>
                    <div className="eye right"></div>
                  </div>
                  <div className="avatar-mouth"></div>
                </div>
              </div>
              
              <div className="avatar-stats">
                <div className="avatar-stat">
                  <span className="stat-label">Animation:</span>
                  <span className="stat-value">{avatar.animation_state}</span>
                </div>
                <div className="avatar-stat">
                  <span className="stat-label">Size:</span>
                  <span className="stat-value">{(avatar.size * 100).toFixed(0)}%</span>
                </div>
                <div className="avatar-stat">
                  <span className="stat-label">Glow:</span>
                  <span className="stat-value">{(avatar.glow_intensity * 100).toFixed(0)}%</span>
                </div>
                <div className="avatar-stat">
                  <span className="stat-label">Primary Color:</span>
                  <span 
                    className="stat-value color-preview"
                    style={{ backgroundColor: avatar.primary_color }}
                  ></span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Landmarks */}
        {landscape?.landmarks && landscape.landmarks.length > 0 && (
          <div className="landmarks-section">
            <h3>Emotional Landmarks</h3>
            <div className="landmarks-list">
              {landscape.landmarks.slice(-5).map((landmark, index) => (
                <div key={index} className="landmark-card">
                  <div className="landmark-header">
                    <span className="landmark-emotion">{landmark.position.emotion}</span>
                    <span className="landmark-intensity">{(landmark.position.intensity * 100).toFixed(0)}%</span>
                  </div>
                  <p className="landmark-description">{landmark.description}</p>
                  <span className="landmark-time">
                    {new Date(landmark.timestamp).toLocaleDateString()}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Emotional Boundaries */}
        <div className="boundaries-section">
          <h3>Your Emotional Boundaries</h3>
          <div className="boundaries-display">
            <div className="boundary">
              <span className="boundary-label">Valence Range:</span>
              <span className="boundary-value">-1.0 to +1.0</span>
            </div>
            <div className="boundary">
              <span className="boundary-label">Arousal Range:</span>
              <span className="boundary-value">-1.0 to +1.0</span>
            </div>
            <div className="boundary">
              <span className="boundary-label">Dominance Range:</span>
              <span className="boundary-value">-1.0 to +1.0</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ThreeDMapping; 