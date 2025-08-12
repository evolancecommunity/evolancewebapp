import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../App';
import axios from 'axios';

const AICheckIn = ({ onResponse }) => {
  const { API } = useContext(AuthContext);
  const [checkin, setCheckin] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [userResponse, setUserResponse] = useState('');
  const [responding, setResponding] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);

  useEffect(() => {
    fetchCheckIn();
  }, []);

  const fetchCheckIn = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API}/ai/checkin`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setCheckin(response.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching check-in:', err);
      setError('Unable to load wellbeing check-in');
    } finally {
      setLoading(false);
    }
  };

  const handleResponse = async () => {
    if (!userResponse.trim()) return;

    try {
      setResponding(true);
      const token = localStorage.getItem('token');
      
      await axios.post(`${API}/chat/message`, {
        message: userResponse
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (onResponse) {
        onResponse(userResponse);
      }

      setUserResponse('');
      setTimeout(() => {
        fetchCheckIn();
      }, 2000);

    } catch (err) {
      console.error('Error sending response:', err);
    } finally {
      setResponding(false);
    }
  };

  const handleSkip = () => {
    fetchCheckIn();
  };

  const handleDismiss = () => {
    setCheckin(null);
    setUserResponse('');
    setIsExpanded(false);
  };

  const getMoodIcon = (tone) => {
    switch (tone) {
      case 'caring':
        return '💙';
      case 'celebratory':
        return '✨';
      case 'gentle':
        return '🌸';
      case 'friendly':
        return '👋';
      case 'supportive':
        return '🤗';
      default:
        return '💭';
    }
  };

  const getMoodColor = (tone) => {
    switch (tone) {
      case 'caring':
        return 'from-blue-500 to-blue-600';
      case 'celebratory':
        return 'from-purple-500 to-purple-600';
      case 'gentle':
        return 'from-pink-500 to-pink-600';
      case 'friendly':
        return 'from-green-500 to-green-600';
      case 'supportive':
        return 'from-indigo-500 to-indigo-600';
      default:
        return 'from-slate-500 to-slate-600';
    }
  };

  if (loading) {
    return (
      <div className="bg-slate-800/50 backdrop-blur-lg border border-slate-700/50 rounded-xl p-4">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          </div>
          <div className="flex-1">
            <div className="h-4 bg-slate-700 rounded animate-pulse"></div>
            <div className="h-3 bg-slate-700 rounded animate-pulse mt-2 w-2/3"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-900/20 border border-red-700/50 rounded-xl p-4">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-red-500 rounded-full flex items-center justify-center">
            <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div className="flex-1">
            <p className="text-red-300 text-sm">{error}</p>
          </div>
          <button
            onClick={fetchCheckIn}
            className="text-red-300 hover:text-white text-sm font-medium"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (!checkin) {
    return null;
  }

  return (
    <div className={`bg-slate-800/50 backdrop-blur-lg border border-slate-700/50 rounded-xl transition-all duration-300 ${
      isExpanded ? 'p-6' : 'p-4'
    }`}>
      {/* Header */}
      <div className="flex items-center space-x-3">
        <div className={`w-10 h-10 bg-gradient-to-r ${getMoodColor(checkin.tone)} rounded-full flex items-center justify-center`}>
          <span className="text-white text-lg">{getMoodIcon(checkin.tone)}</span>
        </div>
        
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between">
            <h3 className="text-white font-medium text-sm">Wellbeing Check-in</h3>
            <span className="text-slate-400 text-xs">
              {new Date(checkin.timestamp).toLocaleTimeString([], { 
                hour: '2-digit', 
                minute: '2-digit' 
              })}
            </span>
          </div>
          
          {!isExpanded && (
            <p className="text-slate-300 text-sm mt-1 line-clamp-2">
              {checkin.message}
            </p>
          )}
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="text-slate-400 hover:text-white transition-colors duration-200"
          >
            <svg className={`w-4 h-4 transform transition-transform duration-200 ${
              isExpanded ? 'rotate-180' : ''
            }`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          
          <button
            onClick={handleDismiss}
            className="text-slate-400 hover:text-white transition-colors duration-200"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      {/* Expanded Content */}
      {isExpanded && (
        <div className="mt-4 space-y-4">
          {/* Message */}
          <div className="bg-slate-700/30 rounded-lg p-4">
            <p className="text-slate-200 text-sm leading-relaxed">
              {checkin.message}
            </p>
          </div>

          {/* Response Input */}
          <div className="space-y-3">
            <textarea
              value={userResponse}
              onChange={(e) => setUserResponse(e.target.value)}
              placeholder="Share how you're feeling or what's on your mind..."
              className="w-full p-3 bg-slate-700/50 border border-slate-600 text-slate-200 placeholder-slate-400 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
              rows="3"
              disabled={responding}
            />
            
            <div className="flex items-center justify-between">
              <div className="text-slate-500 text-xs">
                {userResponse.length}/500 characters
              </div>
              
              <div className="flex items-center space-x-2">
                <button
                  onClick={handleSkip}
                  disabled={responding}
                  className="px-3 py-2 text-slate-400 hover:text-white text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
                >
                  Skip
                </button>
                
                <button
                  onClick={handleResponse}
                  disabled={!userResponse.trim() || responding}
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 disabled:cursor-not-allowed text-white text-sm font-medium rounded-lg transition-all duration-200 flex items-center space-x-2"
                >
                  {responding ? (
                    <>
                      <div className="w-3 h-3 border border-white border-t-transparent rounded-full animate-spin"></div>
                      <span>Sending...</span>
                    </>
                  ) : (
                    <span>Share</span>
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Quick Response Suggestions */}
          <div className="space-y-2">
            <p className="text-slate-400 text-xs font-medium">Quick responses:</p>
            <div className="flex flex-wrap gap-2">
              {[
                "I'm feeling good today, thank you",
                "I'm a bit stressed but managing",
                "I'm excited about something",
                "I'm feeling overwhelmed",
                "I'm grateful for today"
              ].map((suggestion, index) => (
                <button
                  key={index}
                  onClick={() => setUserResponse(suggestion)}
                  className="px-3 py-1 bg-slate-700/50 hover:bg-slate-600/50 text-slate-300 text-xs rounded-full transition-colors duration-200"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AICheckIn; 