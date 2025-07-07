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
      setError('Failed to load check-in message');
    } finally {
      setLoading(false);
    }
  };

  const handleResponse = async () => {
    if (!userResponse.trim()) return;

    try {
      setResponding(true);
      const token = localStorage.getItem('token');
      
      // Send response to chat endpoint
      await axios.post(`${API}/chat/message`, {
        message: userResponse
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });

      // Call parent callback if provided
      if (onResponse) {
        onResponse(userResponse);
      }

      // Clear input and fetch new check-in
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

  const getToneIcon = (tone) => {
    switch (tone) {
      case 'caring':
        return '💜';
      case 'celebratory':
        return '🎉';
      case 'gentle':
        return '🌸';
      case 'friendly':
        return '👋';
      default:
        return '💭';
    }
  };

  if (loading) {
    return (
      <div className="glass-effect rounded-2xl p-6 spiritual-glow">
        <div className="text-center">
          <div className="chakra-loading w-12 h-12 mx-auto mb-4"></div>
          <p className="text-purple-200">Preparing your check-in...</p>
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
            onClick={fetchCheckIn}
            className="spiritual-button text-white font-medium py-2 px-4 rounded-lg"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (!checkin) {
    return (
      <div className="glass-effect rounded-2xl p-6 spiritual-glow">
        <div className="text-center">
          <p className="text-purple-200">No check-in available at the moment.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="glass-effect rounded-2xl p-6 spiritual-glow">
      {/* Check-in Header */}
      <div className="flex items-center mb-4">
        <div className="w-12 h-12 bg-gradient-to-r from-purple-400 to-cyan-400 rounded-full flex items-center justify-center mr-4">
          <span className="text-white text-xl font-bold">E</span>
        </div>
        <div>
          <h3 className="text-white font-semibold">Evolance Check-in</h3>
          <p className="text-purple-300 text-sm">
            {new Date(checkin.timestamp).toLocaleTimeString([], { 
              hour: '2-digit', 
              minute: '2-digit' 
            })}
          </p>
        </div>
        <div className="ml-auto text-2xl">
          {getToneIcon(checkin.tone)}
        </div>
      </div>

      {/* Check-in Message */}
      <div className="mb-6">
        <p className="text-white text-lg leading-relaxed">
          {checkin.message}
        </p>
      </div>

      {/* Response Input */}
      <div className="space-y-4">
        <div className="relative">
          <textarea
            value={userResponse}
            onChange={(e) => setUserResponse(e.target.value)}
            placeholder="Share how you're feeling..."
            className="w-full p-4 bg-white bg-opacity-10 border border-purple-300 border-opacity-30 rounded-lg text-white placeholder-purple-300 resize-none focus:outline-none focus:border-purple-400 focus:bg-opacity-20 transition-all duration-200"
            rows="3"
            disabled={responding}
          />
          <div className="absolute bottom-2 right-2 text-purple-300 text-xs">
            {userResponse.length}/500
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex space-x-3">
          <button
            onClick={handleResponse}
            disabled={!userResponse.trim() || responding}
            className="flex-1 spiritual-button text-white font-medium py-3 px-4 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
          >
            {responding ? (
              <span className="flex items-center justify-center">
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                Sending...
              </span>
            ) : (
              'Share Response'
            )}
          </button>
          
          <button
            onClick={handleSkip}
            disabled={responding}
            className="px-4 py-3 bg-gray-600 hover:bg-gray-700 text-white font-medium rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
          >
            Skip
          </button>
        </div>
      </div>

      {/* Quick Response Buttons */}
      <div className="mt-4">
        <p className="text-purple-300 text-sm mb-2">Quick responses:</p>
        <div className="flex flex-wrap gap-2">
          {[
            "I'm doing well, thank you!",
            "I'm feeling a bit down today",
            "I'm excited about something",
            "I'm feeling anxious",
            "I'm grateful for today"
          ].map((quickResponse, index) => (
            <button
              key={index}
              onClick={() => setUserResponse(quickResponse)}
              disabled={responding}
              className="px-3 py-1 bg-purple-600 bg-opacity-30 hover:bg-opacity-50 text-white text-sm rounded-full transition-all duration-200 disabled:opacity-50"
            >
              {quickResponse}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AICheckIn; 