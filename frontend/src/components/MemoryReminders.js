import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../App';
import axios from 'axios';

const MemoryReminders = ({ onMemoryClick }) => {
  const { API } = useContext(AuthContext);
  const [reminders, setReminders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showAll, setShowAll] = useState(false);

  useEffect(() => {
    fetchReminders();
  }, []);

  const fetchReminders = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API}/ai/reminder`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      // Handle single reminder or array of reminders
      const reminderData = response.data;
      if (reminderData) {
        setReminders(Array.isArray(reminderData) ? reminderData : [reminderData]);
      } else {
        setReminders([]);
      }
      setError(null);
    } catch (err) {
      console.error('Error fetching reminders:', err);
      setError('Failed to load memory reminders');
      setReminders([]);
    } finally {
      setLoading(false);
    }
  };

  const handleMemoryClick = (reminder) => {
    if (onMemoryClick) {
      onMemoryClick(reminder);
    }
  };

  const getEmotionIcon = (emotion) => {
    const icons = {
      joy: '😊',
      love: '💖',
      surprise: '😲',
      neutral: '😐',
      sadness: '😢',
      fear: '😨',
      anger: '😠'
    };
    return icons[emotion] || '💭';
  };

  const getEmotionColor = (emotion) => {
    const colors = {
      joy: 'from-yellow-400 to-orange-400',
      love: 'from-pink-400 to-red-400',
      surprise: 'from-cyan-400 to-blue-400',
      neutral: 'from-gray-400 to-gray-500',
      sadness: 'from-blue-400 to-indigo-400',
      fear: 'from-purple-400 to-indigo-400',
      anger: 'from-red-400 to-orange-400'
    };
    return colors[emotion] || 'from-gray-400 to-gray-500';
  };

  const formatDate = (dateString) => {
    try {
      const date = new Date(dateString);
      const now = new Date();
      const diffTime = Math.abs(now - date);
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      
      if (diffDays === 1) {
        return 'Yesterday';
      } else if (diffDays < 7) {
        return `${diffDays} days ago`;
      } else if (diffDays < 30) {
        const weeks = Math.floor(diffDays / 7);
        return `${weeks} week${weeks > 1 ? 's' : ''} ago`;
      } else {
        return date.toLocaleDateString();
      }
    } catch (e) {
      return 'Recently';
    }
  };

  if (loading) {
    return (
      <div className="glass-effect rounded-2xl p-6 spiritual-glow">
        <div className="text-center">
          <div className="chakra-loading w-12 h-12 mx-auto mb-4"></div>
          <p className="text-purple-200">Loading your memories...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="glass-effect rounded-2xl p-6 spiritual-glow">
        <div className="text-center">
          <p className="text-red-400 mb-4">{error}</p>
          <button
            onClick={fetchReminders}
            className="spiritual-button text-white font-medium py-2 px-4 rounded-lg"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (reminders.length === 0) {
    return (
      <div className="glass-effect rounded-2xl p-6 spiritual-glow">
        <div className="text-center">
          <div className="text-4xl mb-4">🌟</div>
          <h3 className="text-white font-semibold mb-2">No Memories Yet</h3>
          <p className="text-purple-200 text-sm">
            Continue your journey to unlock beautiful memories and milestones.
          </p>
        </div>
      </div>
    );
  }

  const displayedReminders = showAll ? reminders : reminders.slice(0, 3);

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-semibold text-white flex items-center">
          <span className="mr-2">💫</span>
          Memory Reminders
        </h3>
        {reminders.length > 3 && (
          <button
            onClick={() => setShowAll(!showAll)}
            className="text-purple-300 hover:text-white text-sm transition-colors duration-200"
          >
            {showAll ? 'Show Less' : `Show All (${reminders.length})`}
          </button>
        )}
      </div>

      {/* Reminders List */}
      <div className="space-y-4">
        {displayedReminders.map((reminder, index) => (
          <div
            key={index}
            className="glass-effect rounded-xl p-4 spiritual-glow cursor-pointer transform hover:scale-105 transition-all duration-300"
            onClick={() => handleMemoryClick(reminder)}
          >
            <div className="flex items-start space-x-4">
              {/* Emotion Icon */}
              <div className={`w-12 h-12 rounded-full bg-gradient-to-r ${getEmotionColor(reminder.emotion)} flex items-center justify-center text-2xl flex-shrink-0`}>
                {getEmotionIcon(reminder.emotion)}
              </div>

              {/* Content */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="text-white font-semibold text-lg">
                    {reminder.title}
                  </h4>
                  <span className="text-purple-300 text-xs">
                    {formatDate(reminder.memory_date)}
                  </span>
                </div>
                
                <p className="text-purple-200 text-sm leading-relaxed mb-3">
                  {reminder.message}
                </p>

                {/* Memory Date */}
                <div className="flex items-center text-purple-300 text-xs">
                  <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  Memory from {formatDate(reminder.memory_date)}
                </div>
              </div>

              {/* Click Indicator */}
              <div className="text-purple-300 opacity-50">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Empty State for No More Reminders */}
      {showAll && reminders.length === 0 && (
        <div className="text-center py-8">
          <div className="text-4xl mb-4">🌟</div>
          <p className="text-purple-200">No more memories to show right now.</p>
        </div>
      )}

      {/* Refresh Button */}
      <div className="text-center pt-4">
        <button
          onClick={fetchReminders}
          className="spiritual-button text-white font-medium py-2 px-4 rounded-lg transition-all duration-200"
        >
          Refresh Memories
        </button>
      </div>
    </div>
  );
};

export default MemoryReminders; 