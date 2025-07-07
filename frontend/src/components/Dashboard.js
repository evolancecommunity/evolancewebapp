import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../App';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import AvatarVisualization from './AvatarVisualization';
import AICheckIn from './AICheckIn';
import MemoryReminders from './MemoryReminders';
import EmotionalProfile from './EmotionalProfile';

const Dashboard = () => {
  const [userProgress, setUserProgress] = useState([]);
  const [emotionalState, setEmotionalState] = useState({
    current_mood: 'contemplative',
    clarity_level: 72,
    fulfillment_level: 68,
    growth_milestones: []
  });
  const [consciousnessJourney, setConsciousnessJourney] = useState({
    past_reflections: [],
    present_decisions: [],
    future_visions: []
  });
  const [loading, setLoading] = useState(true);
  const [activeJourney, setActiveJourney] = useState('present');

  const { user, logout, API } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };

      const [emotionalRes, journeyRes] = await Promise.all([
        axios.get(`${API}/ai/emotional-state`, { headers }),
        axios.get(`${API}/consciousness/journey`, { headers })
      ]);

      setEmotionalState(emotionalRes.data);
      setConsciousnessJourney(journeyRes.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      // Set beautiful demo data
      setEmotionalState({
        current_mood: 'contemplative',
        clarity_level: 72,
        fulfillment_level: 68,
        growth_milestones: [
          { id: 1, title: 'Started your journey', date: 'Today', type: 'beginning', emoji: '🌱' },
          { id: 2, title: 'Completed personality assessment', date: 'Today', type: 'self-discovery', emoji: '🔍' },
          { id: 3, title: 'First moment of clarity', date: 'Today', type: 'breakthrough', emoji: '💫' }
        ]
      });
      setConsciousnessJourney({
        past_reflections: [
          { id: 1, title: 'A moment of courage', description: 'When you stood up for yourself and felt proud', impact: 'positive', emoji: '🦁' },
          { id: 2, title: 'A learning experience', description: 'A challenge that made you stronger and wiser', impact: 'growth', emoji: '📚' }
        ],
        present_decisions: [
          { id: 1, title: 'Setting healthy boundaries', description: 'Learning to say no with love and respect', status: 'in-progress', emoji: '🛡️' },
          { id: 2, title: 'Building self-care routine', description: 'Creating daily practices that nourish your soul', status: 'planning', emoji: '💆‍♀️' }
        ],
        future_visions: [
          { id: 1, title: 'Authentic self-expression', description: 'Living in perfect alignment with your true values', timeline: '3 months', emoji: '🎭' },
          { id: 2, title: 'Emotional resilience', description: 'Navigating life\'s challenges with grace and wisdom', timeline: '6 months', emoji: '🌊' }
        ]
      });
      setLoading(false);
    }
  };

  const getMoodEmoji = (mood) => {
    const moodMap = {
      'joyful': '😊',
      'contemplative': '🤔',
      'peaceful': '😌',
      'excited': '🤩',
      'grateful': '🙏',
      'curious': '🤓',
      'neutral': '😐',
      'tired': '😴',
      'stressed': '😰'
    };
    return moodMap[mood] || '😊';
  };

  const getMoodColor = (mood) => {
    const colorMap = {
      'joyful': 'from-yellow-400 to-orange-400',
      'contemplative': 'from-purple-400 to-indigo-400',
      'peaceful': 'from-blue-400 to-cyan-400',
      'excited': 'from-pink-400 to-red-400',
      'grateful': 'from-green-400 to-emerald-400',
      'curious': 'from-indigo-400 to-purple-400',
      'neutral': 'from-gray-400 to-slate-400',
      'tired': 'from-blue-400 to-indigo-400',
      'stressed': 'from-red-400 to-pink-400'
    };
    return colorMap[mood] || 'from-purple-400 to-indigo-400';
  };

  const getJourneyStageInfo = (stage) => {
    const stages = {
      past: {
        title: 'The Past',
        subtitle: 'Reflect on formative memories',
        description: 'Explore how your experiences have shaped who you are today',
        gradient: 'from-red-500 via-pink-500 to-purple-500',
        bgGradient: 'from-red-50 to-pink-50',
        icon: '🕰️',
        buttonColor: 'bg-red-500 hover:bg-red-600'
      },
      present: {
        title: 'The Present',
        subtitle: 'Make conscious decisions',
        description: 'Navigate current challenges with clarity and self-awareness',
        gradient: 'from-blue-500 via-cyan-500 to-teal-500',
        bgGradient: 'from-blue-50 to-cyan-50',
        icon: '✨',
        buttonColor: 'bg-blue-500 hover:bg-blue-600'
      },
      future: {
        title: 'The Future',
        subtitle: 'Visualize identity growth',
        description: 'Set intentions for the person you want to become',
        gradient: 'from-green-500 via-emerald-500 to-teal-500',
        bgGradient: 'from-green-50 to-emerald-50',
        icon: '🌟',
        buttonColor: 'bg-green-500 hover:bg-green-600'
      }
    };
    return stages[stage];
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-700 to-indigo-800 flex items-center justify-center">
        <div className="text-center">
          <div className="relative">
            <div className="w-20 h-20 border-4 border-purple-200 border-t-purple-600 rounded-full animate-spin mx-auto mb-6"></div>
            <div className="absolute inset-0 w-20 h-20 border-4 border-transparent border-t-pink-400 rounded-full animate-spin mx-auto" style={{ animationDirection: 'reverse', animationDuration: '1.5s' }}></div>
          </div>
          <p className="text-white text-xl font-medium">Loading your consciousness journey...</p>
          <p className="text-purple-200 text-sm mt-2">Preparing your personalized experience</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-700 to-indigo-800 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-20 left-20 w-72 h-72 bg-purple-400 rounded-full opacity-10 blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-pink-400 rounded-full opacity-10 blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/3 right-1/4 w-64 h-64 bg-indigo-400 rounded-full opacity-10 blur-3xl animate-pulse delay-500"></div>
        <div className="absolute bottom-1/3 left-1/4 w-80 h-80 bg-cyan-400 rounded-full opacity-10 blur-3xl animate-pulse delay-1500"></div>
      </div>

      {/* Header */}
      <header className="relative z-20 bg-white/10 backdrop-blur-xl border-b border-white/20 sticky top-0">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <div className="flex items-center">
                <div className="relative">
                  <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mr-4 shadow-lg">
                    <span className="text-white font-bold text-xl">E</span>
                  </div>
                  <div className="absolute -top-1 -right-1 w-4 h-4 bg-gradient-to-r from-yellow-400 to-orange-400 rounded-full animate-pulse"></div>
                </div>
                <div>
                  <h1 className="text-3xl font-bold bg-gradient-to-r from-white to-purple-200 bg-clip-text text-transparent">
                    Evolance
                  </h1>
                  <p className="text-purple-200 text-sm">Your consciousness companion</p>
                </div>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <button
                onClick={() => navigate('/chat')}
                className="p-3 rounded-xl bg-white/10 hover:bg-white/20 transition-all duration-300 backdrop-blur-lg border border-white/20 group"
                title="Chat with Evolance"
              >
                <svg className="w-6 h-6 text-white group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </button>

              <button
                onClick={() => navigate('/consciousness')}
                className="p-3 rounded-xl bg-white/10 hover:bg-white/20 transition-all duration-300 backdrop-blur-lg border border-white/20 group"
                title="Consciousness Timeline"
              >
                <svg className="w-6 h-6 text-white group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </button>

              <button
                onClick={() => navigate('/profile')}
                className="p-3 rounded-xl bg-white/10 hover:bg-white/20 transition-all duration-300 backdrop-blur-lg border border-white/20 group"
                title="Profile"
              >
                <svg className="w-6 h-6 text-white group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </button>

              <button
                onClick={logout}
                className="p-3 rounded-xl bg-red-500/20 hover:bg-red-500/30 transition-all duration-300 backdrop-blur-lg border border-red-400/30 group"
                title="Logout"
              >
                <svg className="w-6 h-6 text-red-300 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Welcome Section */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center px-6 py-3 rounded-full bg-white/10 backdrop-blur-lg border border-white/20 mb-6">
            <span className="text-2xl mr-3">{getMoodEmoji(emotionalState.current_mood)}</span>
            <span className="text-white font-medium capitalize">{emotionalState.current_mood}</span>
          </div>
          <h2 className="text-5xl md:text-6xl font-bold text-white mb-6 leading-tight">
            Welcome back, <span className="bg-gradient-to-r from-purple-300 to-pink-300 bg-clip-text text-transparent">{user?.full_name?.split(' ')[0]}</span>
          </h2>
          <p className="text-xl text-purple-200 max-w-3xl mx-auto leading-relaxed">
            Continue your journey toward emotional clarity and authentic self-expression. 
            Your consciousness journey awaits.
          </p>
        </div>

        {/* Current State Overview */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-16">
          {/* Emotional State Card */}
          <div className="group relative">
            <div className="absolute inset-0 bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-3xl blur-xl group-hover:blur-2xl transition-all duration-500"></div>
            <div className="relative bg-white/10 backdrop-blur-xl rounded-3xl p-8 border border-white/20 hover:border-white/30 transition-all duration-500">
              <div className="flex items-center mb-6">
                <div className={`w-16 h-16 rounded-2xl bg-gradient-to-r ${getMoodColor(emotionalState.current_mood)} flex items-center justify-center mr-4 shadow-lg`}>
                  <span className="text-3xl">{getMoodEmoji(emotionalState.current_mood)}</span>
                </div>
                <div>
                  <h3 className="text-xl font-bold text-white">How you're feeling</h3>
                  <p className="text-purple-200 capitalize">{emotionalState.current_mood}</p>
                </div>
              </div>
              <button
                onClick={() => navigate('/chat', { state: { context: 'emotional-checkin' } })}
                className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-semibold py-4 px-6 rounded-2xl transition-all duration-300 transform hover:scale-105 shadow-lg"
              >
                Share more with Evolance
              </button>
            </div>
          </div>

          {/* Clarity Level Card */}
          <div className="group relative">
            <div className="absolute inset-0 bg-gradient-to-r from-blue-500/20 to-cyan-500/20 rounded-3xl blur-xl group-hover:blur-2xl transition-all duration-500"></div>
            <div className="relative bg-white/10 backdrop-blur-xl rounded-3xl p-8 border border-white/20 hover:border-white/30 transition-all duration-500">
              <h3 className="text-xl font-bold text-white mb-6">Emotional Clarity</h3>
              <div className="mb-6">
                <div className="flex justify-between text-sm mb-3">
                  <span className="text-purple-200">Current level</span>
                  <span className="text-white font-bold text-lg">{emotionalState.clarity_level}%</span>
                </div>
                <div className="relative">
                  <div className="w-full bg-white/20 rounded-full h-4 overflow-hidden">
                    <div 
                      className="h-4 rounded-full bg-gradient-to-r from-blue-400 to-cyan-400 transition-all duration-1000 ease-out shadow-lg"
                      style={{ width: `${emotionalState.clarity_level}%` }}
                    ></div>
                  </div>
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-pulse"></div>
                </div>
              </div>
              <button
                onClick={() => navigate('/consciousness')}
                className="w-full bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 text-white font-semibold py-4 px-6 rounded-2xl transition-all duration-300 transform hover:scale-105 shadow-lg"
              >
                Build more clarity
              </button>
            </div>
          </div>

          {/* Avatar Card */}
          <div className="group relative">
            <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/20 to-purple-500/20 rounded-3xl blur-xl group-hover:blur-2xl transition-all duration-500"></div>
            <div className="relative bg-white/10 backdrop-blur-xl rounded-3xl p-8 border border-white/20 hover:border-white/30 transition-all duration-500">
              <h3 className="text-xl font-bold text-white mb-6 text-center">Your Avatar</h3>
              <div className="flex justify-center mb-6">
                <AvatarVisualization size="large" showDetails={false} />
              </div>
              <button
                onClick={() => navigate('/profile')}
                className="w-full bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 text-white font-semibold py-4 px-6 rounded-2xl transition-all duration-300 transform hover:scale-105 shadow-lg"
              >
                View full profile
              </button>
            </div>
          </div>
        </div>

        {/* Consciousness Journey */}
        <div className="mb-16">
          <div className="text-center mb-12">
            <h3 className="text-4xl font-bold text-white mb-6">Your Consciousness Journey</h3>
            <p className="text-xl text-purple-200 max-w-3xl mx-auto leading-relaxed">
              A guided path through your past, present, and future to build self-awareness and authentic identity
            </p>
          </div>

          {/* Journey Navigation */}
          <div className="flex justify-center mb-12">
            <div className="bg-white/10 backdrop-blur-xl rounded-2xl p-2 border border-white/20">
              {['past', 'present', 'future'].map((stage) => {
                const info = getJourneyStageInfo(stage);
                return (
                  <button
                    key={stage}
                    onClick={() => setActiveJourney(stage)}
                    className={`px-8 py-4 rounded-xl transition-all duration-500 flex items-center font-semibold ${
                      activeJourney === stage
                        ? `bg-gradient-to-r ${info.gradient} text-white shadow-lg transform scale-105`
                        : 'text-purple-200 hover:text-white hover:bg-white/10'
                    }`}
                  >
                    <span className="mr-3 text-xl">{info.icon}</span>
                    {info.title}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Journey Content */}
          <div className="group relative">
            <div className="absolute inset-0 bg-gradient-to-r from-white/5 to-white/10 rounded-3xl blur-2xl group-hover:blur-3xl transition-all duration-500"></div>
            <div className="relative bg-white/10 backdrop-blur-xl rounded-3xl p-12 border border-white/20 hover:border-white/30 transition-all duration-500">
              {activeJourney === 'past' && (
                <div>
                  <div className="text-center mb-12">
                    <h4 className="text-3xl font-bold text-white mb-4">The Past</h4>
                    <p className="text-purple-200 text-lg">Reflect on formative memories and past decisions</p>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {consciousnessJourney.past_reflections.map((reflection) => (
                      <div key={reflection.id} className="group/item bg-white/5 rounded-2xl p-8 hover:bg-white/10 transition-all duration-500 border border-white/10 hover:border-white/20">
                        <div className="flex items-start mb-4">
                          <span className="text-4xl mr-4">{reflection.emoji}</span>
                          <div>
                            <h5 className="text-xl font-bold text-white mb-2">{reflection.title}</h5>
                            <p className="text-purple-200 leading-relaxed">{reflection.description}</p>
                          </div>
                        </div>
                        <span className={`inline-flex items-center px-4 py-2 rounded-full text-sm font-medium ${
                          reflection.impact === 'positive' ? 'bg-green-500/20 text-green-300 border border-green-400/30' : 'bg-blue-500/20 text-blue-300 border border-blue-400/30'
                        }`}>
                          {reflection.impact === 'positive' ? 'Positive Impact' : 'Growth Experience'}
                        </span>
                      </div>
                    ))}
                  </div>
                  <div className="text-center mt-12">
                    <button
                      onClick={() => navigate('/chat', { state: { context: 'past-reflection' } })}
                      className="bg-gradient-to-r from-red-500 to-pink-500 hover:from-red-600 hover:to-pink-600 text-white font-semibold py-4 px-8 rounded-2xl transition-all duration-300 transform hover:scale-105 shadow-lg"
                    >
                      Explore more memories with Evolance
                    </button>
                  </div>
                </div>
              )}

              {activeJourney === 'present' && (
                <div>
                  <div className="text-center mb-12">
                    <h4 className="text-3xl font-bold text-white mb-4">The Present</h4>
                    <p className="text-purple-200 text-lg">Make conscious decisions and explore current feelings</p>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {consciousnessJourney.present_decisions.map((decision) => (
                      <div key={decision.id} className="group/item bg-white/5 rounded-2xl p-8 hover:bg-white/10 transition-all duration-500 border border-white/10 hover:border-white/20">
                        <div className="flex items-start mb-4">
                          <span className="text-4xl mr-4">{decision.emoji}</span>
                          <div>
                            <h5 className="text-xl font-bold text-white mb-2">{decision.title}</h5>
                            <p className="text-purple-200 leading-relaxed">{decision.description}</p>
                          </div>
                        </div>
                        <span className={`inline-flex items-center px-4 py-2 rounded-full text-sm font-medium ${
                          decision.status === 'in-progress' ? 'bg-yellow-500/20 text-yellow-300 border border-yellow-400/30' : 'bg-purple-500/20 text-purple-300 border border-purple-400/30'
                        }`}>
                          {decision.status === 'in-progress' ? 'In Progress' : 'Planning'}
                        </span>
                      </div>
                    ))}
                  </div>
                  <div className="text-center mt-12">
                    <button
                      onClick={() => navigate('/chat', { state: { context: 'present-decision' } })}
                      className="bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 text-white font-semibold py-4 px-8 rounded-2xl transition-all duration-300 transform hover:scale-105 shadow-lg"
                    >
                      Get guidance on current decisions
                    </button>
                  </div>
                </div>
              )}

              {activeJourney === 'future' && (
                <div>
                  <div className="text-center mb-12">
                    <h4 className="text-3xl font-bold text-white mb-4">The Future</h4>
                    <p className="text-purple-200 text-lg">Visualize identity growth and set intentions for the self</p>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {consciousnessJourney.future_visions.map((vision) => (
                      <div key={vision.id} className="group/item bg-white/5 rounded-2xl p-8 hover:bg-white/10 transition-all duration-500 border border-white/10 hover:border-white/20">
                        <div className="flex items-start mb-4">
                          <span className="text-4xl mr-4">{vision.emoji}</span>
                          <div>
                            <h5 className="text-xl font-bold text-white mb-2">{vision.title}</h5>
                            <p className="text-purple-200 leading-relaxed">{vision.description}</p>
                          </div>
                        </div>
                        <span className="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium bg-green-500/20 text-green-300 border border-green-400/30">
                          {vision.timeline} timeline
                        </span>
                      </div>
                    ))}
                  </div>
                  <div className="text-center mt-12">
                    <button
                      onClick={() => navigate('/chat', { state: { context: 'future-vision' } })}
                      className="bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white font-semibold py-4 px-8 rounded-2xl transition-all duration-300 transform hover:scale-105 shadow-lg"
                    >
                      Create your future vision
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Growth Milestones */}
        <div className="group relative mb-16">
          <div className="absolute inset-0 bg-gradient-to-r from-yellow-500/10 to-orange-500/10 rounded-3xl blur-2xl group-hover:blur-3xl transition-all duration-500"></div>
          <div className="relative bg-white/10 backdrop-blur-xl rounded-3xl p-12 border border-white/20 hover:border-white/30 transition-all duration-500">
            <h3 className="text-3xl font-bold text-white mb-8 text-center">Your Growth Milestones</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {emotionalState.growth_milestones.map((milestone) => (
                <div key={milestone.id} className="group/item bg-white/5 rounded-2xl p-8 text-center hover:bg-white/10 transition-all duration-500 border border-white/10 hover:border-white/20 transform hover:scale-105">
                  <div className="text-5xl mb-4 group-hover/item:scale-110 transition-transform duration-300">
                    {milestone.emoji}
                  </div>
                  <h4 className="text-xl font-bold text-white mb-3">{milestone.title}</h4>
                  <p className="text-purple-200 text-sm">{milestone.date}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <button
            onClick={() => navigate('/chat')}
            className="group relative overflow-hidden"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-purple-600 to-indigo-600 rounded-3xl blur-xl group-hover:blur-2xl transition-all duration-500"></div>
            <div className="relative bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-semibold py-8 px-8 rounded-3xl transition-all duration-500 text-left transform hover:scale-105 shadow-2xl">
              <div className="text-4xl mb-4 group-hover:scale-110 transition-transform duration-300">💜</div>
              <h3 className="text-2xl font-bold mb-3">Chat with Evolance</h3>
              <p className="text-purple-100 leading-relaxed">Share your thoughts and get personalized guidance</p>
            </div>
          </button>

          <button
            onClick={() => navigate('/consciousness')}
            className="group relative overflow-hidden"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-3xl blur-xl group-hover:blur-2xl transition-all duration-500"></div>
            <div className="relative bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white font-semibold py-8 px-8 rounded-3xl transition-all duration-500 text-left transform hover:scale-105 shadow-2xl">
              <div className="text-4xl mb-4 group-hover:scale-110 transition-transform duration-300">✨</div>
              <h3 className="text-2xl font-bold mb-3">Consciousness Timeline</h3>
              <p className="text-blue-100 leading-relaxed">Track your emotional growth and decisions</p>
            </div>
          </button>

          <button
            onClick={() => navigate('/profile')}
            className="group relative overflow-hidden"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-green-600 to-emerald-600 rounded-3xl blur-xl group-hover:blur-2xl transition-all duration-500"></div>
            <div className="relative bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white font-semibold py-8 px-8 rounded-3xl transition-all duration-500 text-left transform hover:scale-105 shadow-2xl">
              <div className="text-4xl mb-4 group-hover:scale-110 transition-transform duration-300">📊</div>
              <h3 className="text-2xl font-bold mb-3">Emotional Profile</h3>
              <p className="text-green-100 leading-relaxed">View your emotional patterns and progress</p>
            </div>
          </button>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
