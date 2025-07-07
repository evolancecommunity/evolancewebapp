import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../App';
import axios from 'axios';

const AvatarVisualization = ({ size = 'medium', showDetails = true, className = '' }) => {
  const { API } = useContext(AuthContext);
  const [avatarState, setAvatarState] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAvatarState();
  }, []);

  const fetchAvatarState = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API}/ai/avatar`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setAvatarState(response.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching avatar state:', err);
      setError('Failed to load avatar state');
      // Set default state with beautiful chakra colors
      setAvatarState({
        primary_color: '#8B5CF6', // Purple for crown chakra
        secondary_color: '#EC4899', // Pink for heart chakra
        active_chakra: 'balanced',
        glow_intensity: 7,
        animation_state: 'gentle',
        emotional_state: 'peaceful',
        fulfillment_level: 65
      });
    } finally {
      setLoading(false);
    }
  };

  const getSizeClasses = () => {
    switch (size) {
      case 'small':
        return 'w-20 h-20';
      case 'large':
        return 'w-40 h-40';
      case 'xlarge':
        return 'w-64 h-64';
      default:
        return 'w-32 h-32';
    }
  };

  const getChakraInfo = (chakra) => {
    const chakraInfo = {
      root: { 
        name: 'Root Chakra', 
        element: 'Earth', 
        meaning: 'Grounding & Security',
        color: '#DC2626',
        symbol: '🌱',
        description: 'Connected to your sense of safety and belonging'
      },
      sacral: { 
        name: 'Sacral Chakra', 
        element: 'Water', 
        meaning: 'Creativity & Emotion',
        color: '#EA580C',
        symbol: '🌊',
        description: 'Flowing with creativity and emotional expression'
      },
      solar_plexus: { 
        name: 'Solar Plexus', 
        element: 'Fire', 
        meaning: 'Power & Confidence',
        color: '#D97706',
        symbol: '☀️',
        description: 'Radiating inner strength and self-assurance'
      },
      heart: { 
        name: 'Heart Chakra', 
        element: 'Air', 
        meaning: 'Love & Compassion',
        color: '#059669',
        symbol: '💚',
        description: 'Open to giving and receiving love'
      },
      throat: { 
        name: 'Throat Chakra', 
        element: 'Sound', 
        meaning: 'Expression & Truth',
        color: '#2563EB',
        symbol: '🗣️',
        description: 'Speaking your authentic truth'
      },
      third_eye: { 
        name: 'Third Eye', 
        element: 'Light', 
        meaning: 'Intuition & Wisdom',
        color: '#7C3AED',
        symbol: '👁️',
        description: 'Seeing with inner wisdom and clarity'
      },
      crown: { 
        name: 'Crown Chakra', 
        element: 'Thought', 
        meaning: 'Spirituality & Unity',
        color: '#8B5CF6',
        symbol: '👑',
        description: 'Connected to higher consciousness'
      },
      balanced: { 
        name: 'Balanced State', 
        element: 'All', 
        meaning: 'Harmony & Peace',
        color: '#EC4899',
        symbol: '✨',
        description: 'All chakras in beautiful harmony'
      }
    };
    return chakraInfo[chakra] || chakraInfo.balanced;
  };

  const getAnimationClass = (animationState) => {
    switch (animationState) {
      case 'pulse':
        return 'animate-pulse';
      case 'bounce':
        return 'animate-bounce';
      case 'spin':
        return 'animate-spin';
      case 'gentle':
        return 'animate-pulse';
      default:
        return 'animate-pulse';
    }
  };

  const getEmotionalStateColor = (emotionalState) => {
    const colors = {
      joyful: '#F59E0B', // Amber
      calm: '#10B981', // Emerald
      peaceful: '#8B5CF6', // Purple
      grateful: '#EC4899', // Pink
      hopeful: '#3B82F6', // Blue
      neutral: '#6B7280', // Gray
      thoughtful: '#8B5CF6', // Purple
      contemplative: '#7C3AED', // Violet
      balanced: '#EC4899' // Pink
    };
    return colors[emotionalState] || colors.neutral;
  };

  if (loading) {
    return (
      <div className={`${getSizeClasses()} ${className} flex items-center justify-center`}>
        <div className="w-full h-full bg-gradient-to-br from-purple-400 via-pink-400 to-indigo-400 rounded-full animate-pulse opacity-60"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`${getSizeClasses()} ${className} flex items-center justify-center`}>
        <div className="w-full h-full bg-gradient-to-br from-gray-300 to-gray-400 rounded-full flex items-center justify-center">
          <span className="text-white text-lg">✨</span>
        </div>
      </div>
    );
  }

  const chakraInfo = getChakraInfo(avatarState.active_chakra);
  const glowIntensity = Math.max(1, Math.min(10, avatarState.glow_intensity));
  const emotionalColor = getEmotionalStateColor(avatarState.emotional_state);

  return (
    <div className={`${className} relative`}>
      {/* Avatar Container */}
      <div className={`${getSizeClasses()} relative mx-auto`}>
        {/* Outer Energy Field */}
        <div 
          className="absolute inset-0 rounded-full animate-pulse blur-xl opacity-60"
          style={{
            background: `radial-gradient(circle, ${emotionalColor}30, transparent)`,
            filter: `blur(${glowIntensity * 2}px)`
          }}
        ></div>
        
        {/* Middle Energy Ring */}
        <div 
          className="relative w-full h-full rounded-full p-3 transform hover:scale-105 transition-all duration-700"
          style={{
            background: `conic-gradient(from 0deg, ${chakraInfo.color}40, ${emotionalColor}40, ${chakraInfo.color}40)`,
            animation: 'spin 10s linear infinite'
          }}
        >
          {/* Inner Avatar Circle */}
          <div 
            className={`w-full h-full rounded-full flex items-center justify-center text-white font-bold ${getAnimationClass(avatarState.animation_state)} transition-all duration-700`}
            style={{
              background: `radial-gradient(circle at 30% 30%, ${chakraInfo.color}90, ${emotionalColor}90)`,
              boxShadow: `0 0 ${glowIntensity * 3}px ${chakraInfo.color}60, inset 0 0 ${glowIntensity * 2}px ${emotionalColor}40`
            }}
          >
            {/* Chakra Symbol */}
            <div className="text-center">
              <div className="text-4xl mb-2 filter drop-shadow-lg">
                {chakraInfo.symbol}
              </div>
              <div className="text-xs opacity-90 font-medium">
                {avatarState.fulfillment_level}%
              </div>
            </div>
          </div>
        </div>

        {/* Floating Energy Particles */}
        <div className="absolute inset-0 overflow-hidden">
          {[...Array(5)].map((_, i) => (
            <div
              key={i}
              className="absolute w-3 h-3 rounded-full animate-bounce opacity-70"
              style={{
                background: `linear-gradient(45deg, ${chakraInfo.color}, ${emotionalColor})`,
                left: `${15 + i * 20}%`,
                top: `${10 + i * 15}%`,
                animationDelay: `${i * 0.3}s`,
                animationDuration: `${2.5 + i * 0.3}s`
              }}
            ></div>
          ))}
        </div>

        {/* Consciousness Level Indicator */}
        <div 
          className="absolute -top-3 -right-3 w-10 h-10 rounded-full flex items-center justify-center text-xs font-bold text-white shadow-lg"
          style={{
            background: `linear-gradient(135deg, ${chakraInfo.color}, ${emotionalColor})`,
            boxShadow: `0 4px 12px ${chakraInfo.color}40`
          }}
        >
          {avatarState.fulfillment_level}
        </div>

        {/* Emotional State Indicator */}
        <div className="absolute -bottom-2 -left-2 w-8 h-8 rounded-full flex items-center justify-center text-xs">
          <div 
            className="w-full h-full rounded-full animate-pulse"
            style={{
              background: emotionalColor,
              boxShadow: `0 0 8px ${emotionalColor}60`
            }}
          ></div>
        </div>
      </div>

      {/* Details Panel */}
      {showDetails && (
        <div className="mt-6 text-center">
          <h3 className="text-xl font-bold text-gray-900 mb-3">
            {chakraInfo.name}
          </h3>
          <p className="text-gray-600 text-sm mb-2 font-medium">
            Element: {chakraInfo.element}
          </p>
          <p className="text-gray-500 text-xs mb-3 leading-relaxed">
            {chakraInfo.description}
          </p>
          <div className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
               style={{
                 background: `${emotionalColor}15`,
                 color: emotionalColor
               }}>
            <div 
              className="w-2 h-2 rounded-full mr-2 animate-pulse"
              style={{ background: emotionalColor }}
            ></div>
            {avatarState.emotional_state.charAt(0).toUpperCase() + avatarState.emotional_state.slice(1)}
          </div>
        </div>
      )}
    </div>
  );
};

export default AvatarVisualization; 