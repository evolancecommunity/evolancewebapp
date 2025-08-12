import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../App';
import axios from 'axios';

const EmotionalProfile = () => {
  const { API } = useContext(AuthContext);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchEmotionalProfile();
  }, []);

  const fetchEmotionalProfile = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API}/ai/profile`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setProfile(response.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching emotional profile:', err);
      setError('Failed to load emotional profile');
    } finally {
      setLoading(false);
    }
  };

  const getEmotionColor = (emotion) => {
    const colors = {
      joy: '#FFD700',
      love: '#FF69B4',
      surprise: '#00CED1',
      neutral: '#808080',
      sadness: '#4169E1',
      fear: '#9932CC',
      anger: '#DC143C'
    };
    return colors[emotion] || '#808080';
  };

  const getFulfillmentColor = (score) => {
    if (score >= 80) return 'from-green-400 to-green-600';
    if (score >= 60) return 'from-yellow-400 to-yellow-600';
    if (score >= 40) return 'from-orange-400 to-orange-600';
    return 'from-red-400 to-red-600';
  };

  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'ascending':
        return '📈';
      case 'descending':
        return '📉';
      default:
        return '➡️';
    }
  };

  if (loading) {
    return (
      <div className="glass-effect rounded-2xl p-8 spiritual-glow">
        <div className="text-center">
          <div className="chakra-loading w-16 h-16 mx-auto mb-4"></div>
          <p className="text-white text-lg">Loading your emotional profile...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="glass-effect rounded-2xl p-8 spiritual-glow">
        <div className="text-center">
          <p className="text-red-400 mb-4">{error}</p>
          <button
            onClick={fetchEmotionalProfile}
            className="spiritual-button text-white font-medium py-2 px-4 rounded-lg"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="glass-effect rounded-2xl p-8 spiritual-glow">
        <div className="text-center">
          <p className="text-purple-200">No emotional data available yet. Start chatting to build your profile!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-white mb-4">Your Emotional Profile</h2>
        <p className="text-purple-200">Your unique emotional fingerprint and growth journey</p>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="glass-effect rounded-2xl p-6 text-center spiritual-glow">
          <div className="text-3xl font-bold text-white mb-2">{profile.total_interactions}</div>
          <div className="text-purple-300">Total Interactions</div>
        </div>

        <div className="glass-effect rounded-2xl p-6 text-center spiritual-glow">
          <div className="text-3xl font-bold text-white mb-2 capitalize">{profile.dominant_emotion}</div>
          <div className="text-purple-300">Dominant Emotion</div>
        </div>

        <div className="glass-effect rounded-2xl p-6 text-center spiritual-glow">
          <div className="text-3xl font-bold text-white mb-2">{profile.emotional_balance_score}</div>
          <div className="text-purple-300">Balance Score</div>
          <div className="w-full bg-black bg-opacity-30 rounded-full h-2 mt-2">
            <div 
              className={`h-2 rounded-full bg-gradient-to-r ${getFulfillmentColor(profile.emotional_balance_score)} transition-all duration-500`}
              style={{ width: `${profile.emotional_balance_score}%` }}
            ></div>
          </div>
        </div>

        <div className="glass-effect rounded-2xl p-6 text-center spiritual-glow">
          <div className="text-3xl font-bold text-white mb-2">{getTrendIcon(profile.fulfillment_trend)}</div>
          <div className="text-purple-300 capitalize">{profile.fulfillment_trend} Trend</div>
        </div>
      </div>

      {/* Emotional Fingerprint */}
      <div className="glass-effect rounded-2xl p-8 spiritual-glow">
        <h3 className="text-2xl font-semibold text-white mb-6 flex items-center">
          <span className="mr-3">🎨</span>
          Emotional Fingerprint
        </h3>
        
        {Object.keys(profile.emotional_fingerprint).length > 0 ? (
          <div className="space-y-4">
            {Object.entries(profile.emotional_fingerprint)
              .sort(([,a], [,b]) => b - a)
              .map(([emotion, count]) => (
                <div key={emotion} className="flex items-center space-x-4">
                  <div 
                    className="w-4 h-4 rounded-full"
                    style={{ backgroundColor: getEmotionColor(emotion) }}
                  ></div>
                  <span className="text-white capitalize flex-1">{emotion}</span>
                  <div className="flex-1 bg-black bg-opacity-30 rounded-full h-3">
                    <div 
                      className="h-3 rounded-full transition-all duration-500"
                      style={{ 
                        width: `${(count / Math.max(...Object.values(profile.emotional_fingerprint))) * 100}%`,
                        backgroundColor: getEmotionColor(emotion)
                      }}
                    ></div>
                  </div>
                  <span className="text-purple-300 text-sm w-12 text-right">{count}</span>
                </div>
              ))}
          </div>
        ) : (
          <p className="text-purple-200 text-center">No emotional data available yet</p>
        )}
      </div>

      {/* Recent Emotions Timeline */}
      <div className="glass-effect rounded-2xl p-8 spiritual-glow">
        <h3 className="text-2xl font-semibold text-white mb-6 flex items-center">
          <span className="mr-3">📊</span>
          Recent Emotional Journey
        </h3>
        
        {profile.recent_emotions.length > 0 ? (
          <div className="flex space-x-2 overflow-x-auto pb-4">
            {profile.recent_emotions.map((emotion, index) => (
              <div
                key={index}
                className="flex-shrink-0 text-center"
                title={`${emotion} - ${profile.recent_emotions.length - index} interactions ago`}
              >
                <div 
                  className="w-8 h-8 rounded-full mb-2 flex items-center justify-center text-white text-xs font-bold"
                  style={{ backgroundColor: getEmotionColor(emotion) }}
                >
                  {emotion.charAt(0).toUpperCase()}
                </div>
                <div className="text-purple-300 text-xs">
                  {profile.recent_emotions.length - index}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-purple-200 text-center">No recent emotional data</p>
        )}
      </div>

      {/* Growth Milestones */}
      {profile.growth_milestones.length > 0 && (
        <div className="glass-effect rounded-2xl p-8 spiritual-glow">
          <h3 className="text-2xl font-semibold text-white mb-6 flex items-center">
            <span className="mr-3">🏆</span>
            Growth Milestones
          </h3>
          
          <div className="space-y-4">
            {profile.growth_milestones.map((milestone, index) => (
              <div key={index} className="flex items-start space-x-4 p-4 bg-white bg-opacity-5 rounded-lg">
                <div className="text-2xl">{milestone.icon}</div>
                <div className="flex-1">
                  <h4 className="text-white font-semibold mb-1">{milestone.title}</h4>
                  <p className="text-purple-200 text-sm mb-2">{milestone.description}</p>
                  <p className="text-purple-300 text-xs">
                    Achieved: {new Date(milestone.achieved_at).toLocaleDateString()}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Refresh Button */}
      <div className="text-center">
        <button
          onClick={fetchEmotionalProfile}
          className="spiritual-button text-white font-medium py-3 px-6 rounded-lg transition-all duration-200"
        >
          Refresh Profile
        </button>
      </div>
    </div>
  );
};

export default EmotionalProfile; 