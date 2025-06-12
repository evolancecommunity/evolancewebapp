import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../App';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Dashboard = () => {
  const [stories, setStories] = useState([]);
  const [userProgress, setUserProgress] = useState([]);
  const [todos, setTodos] = useState([]);
  const [showLeftPanel, setShowLeftPanel] = useState(false);
  const [showRightPanel, setShowRightPanel] = useState(false);
  const [selectedStory, setSelectedStory] = useState(null);
  const [loading, setLoading] = useState(true);

  const { user, logout, API } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };

      const [storiesRes, progressRes, todosRes] = await Promise.all([
        axios.get(`${API}/stories`, { headers }),
        axios.get(`${API}/stories/progress`, { headers }),
        axios.get(`${API}/todos`, { headers })
      ]);

      setStories(storiesRes.data);
      setUserProgress(progressRes.data);
      setTodos(todosRes.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      setLoading(false);
    }
  };

  const startStory = async (storyId) => {
    try {
      const token = localStorage.getItem('token');
      await axios.post(`${API}/stories/${storyId}/start`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchDashboardData();
    } catch (error) {
      console.error('Error starting story:', error);
    }
  };

  const getProgressForStory = (storyId) => {
    return userProgress.find(p => p.story_id === storyId);
  };

  const getProgressColor = (acceptanceLevel) => {
    if (acceptanceLevel >= 80) return 'from-green-400 to-green-600';
    if (acceptanceLevel >= 60) return 'from-yellow-400 to-yellow-600';
    if (acceptanceLevel >= 40) return 'from-orange-400 to-orange-600';
    return 'from-red-400 to-red-600';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-700 to-indigo-800 flex items-center justify-center">
        <div className="text-center">
          <div className="chakra-loading w-16 h-16 mx-auto mb-4"></div>
          <p className="text-white text-lg">Loading your spiritual journey...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-700 to-indigo-800 relative overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-20 left-20 w-40 h-40 bg-purple-400 rounded-full opacity-10 blur-xl animate-pulse"></div>
        <div className="absolute bottom-20 right-20 w-60 h-60 bg-indigo-400 rounded-full opacity-10 blur-xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/3 right-1/4 w-32 h-32 bg-purple-300 rounded-full opacity-10 blur-xl animate-pulse delay-500"></div>
      </div>

      {/* Header */}
      <header className="relative z-20 bg-white bg-opacity-10 backdrop-filter backdrop-blur-lg border-b border-purple-300 border-opacity-30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              {/* Left Panel Toggle */}
              <button
                onClick={() => setShowLeftPanel(!showLeftPanel)}
                className="mr-4 p-2 rounded-lg bg-white bg-opacity-20 hover:bg-opacity-30 transition-all duration-200"
              >
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>

              {/* Logo */}
              <div className="flex items-center">
                <svg width="40" height="20" viewBox="0 0 120 60" className="mr-3">
                  <defs>
                    <linearGradient id="headerInfinityGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                      <stop offset="0%" stopColor="#a78bfa" />
                      <stop offset="50%" stopColor="#ffffff" />
                      <stop offset="100%" stopColor="#c084fc" />
                    </linearGradient>
                  </defs>
                  <path
                    d="M20,30 C20,20 30,10 40,10 C50,10 60,20 60,30 C60,20 70,10 80,10 C90,10 100,20 100,30 C100,40 90,50 80,50 C70,50 60,40 60,30 C60,40 50,50 40,50 C30,50 20,40 20,30 Z"
                    fill="url(#headerInfinityGradient)"
                  />
                </svg>
                <h1 className="text-2xl font-bold text-white">Evolance</h1>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              {/* Navigation Buttons */}
              <button
                onClick={() => navigate('/chat')}
                className="p-2 rounded-lg bg-white bg-opacity-20 hover:bg-opacity-30 transition-all duration-200"
                title="Chat with Evolance"
              >
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </button>

              <button
                onClick={() => navigate('/videos')}
                className="p-2 rounded-lg bg-white bg-opacity-20 hover:bg-opacity-30 transition-all duration-200"
                title="Video Lessons"
              >
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1.01M15 10h1.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </button>

              <button
                onClick={() => navigate('/profile')}
                className="p-2 rounded-lg bg-white bg-opacity-20 hover:bg-opacity-30 transition-all duration-200"
                title="Profile"
              >
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </button>

              {/* Right Panel Toggle */}
              <button
                onClick={() => setShowRightPanel(!showRightPanel)}
                className="p-2 rounded-lg bg-white bg-opacity-20 hover:bg-opacity-30 transition-all duration-200"
                title="Todo List"
              >
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                </svg>
              </button>

              <button
                onClick={logout}
                className="p-2 rounded-lg bg-red-500 bg-opacity-30 hover:bg-opacity-50 transition-all duration-200"
                title="Logout"
              >
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="relative z-10 flex-1 p-6">
        <div className="max-w-7xl mx-auto">
          {/* Welcome Section */}
          <div className="text-center mb-12">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
              Welcome back, {user?.full_name?.split(' ')[0]}
            </h2>
            <p className="text-purple-200 text-lg md:text-xl max-w-2xl mx-auto">
              Continue your spiritual journey and embrace the path to inner peace
            </p>
          </div>

          {/* Stories Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {stories.map((story) => {
              const progress = getProgressForStory(story.id);
              const acceptanceLevel = progress?.acceptance_level || 0;
              
              return (
                <div
                  key={story.id}
                  className="story-card glass-effect rounded-2xl p-6 spiritual-glow"
                >
                  <div className="mb-4">
                    <h3 className="text-xl font-semibold text-white mb-2">
                      {story.title}
                    </h3>
                    <p className="text-purple-200 text-sm leading-relaxed">
                      {story.description}
                    </p>
                  </div>

                  <div className="mb-4">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-purple-300 text-sm">Acceptance Level</span>
                      <span className="text-white text-sm font-medium">{acceptanceLevel}%</span>
                    </div>
                    <div className="w-full bg-white bg-opacity-20 rounded-full h-2">
                      <div 
                        className={`h-2 rounded-full bg-gradient-to-r ${getProgressColor(acceptanceLevel)} transition-all duration-500`}
                        style={{ width: `${acceptanceLevel}%` }}
                      ></div>
                    </div>
                  </div>

                  <div className="flex justify-between items-center mb-4">
                    <span className="text-purple-300 text-sm">
                      {story.difficulty_level === 1 ? 'Beginner' : 
                       story.difficulty_level === 2 ? 'Intermediate' : 'Advanced'}
                    </span>
                    <span className="text-purple-300 text-sm">{story.estimated_duration}</span>
                  </div>

                  <div className="space-y-2">
                    {!progress ? (
                      <button
                        onClick={() => startStory(story.id)}
                        className="w-full spiritual-button text-white font-medium py-2 px-4 rounded-lg transition-all duration-200"
                      >
                        Begin Journey
                      </button>
                    ) : (
                      <div className="space-y-2">
                        {progress.status === 'completed' && progress.ai_confirmed ? (
                          <div className="text-center">
                            <div className="text-green-400 font-medium mb-2">✓ Journey Complete</div>
                            <button
                              onClick={() => navigate('/chat', { state: { storyContext: story.id } })}
                              className="w-full bg-purple-600 hover:bg-purple-700 text-white font-medium py-2 px-4 rounded-lg transition-all duration-200"
                            >
                              Revisit with Evolance
                            </button>
                          </div>
                        ) : (
                          <button
                            onClick={() => navigate('/chat', { state: { storyContext: story.id } })}
                            className="w-full spiritual-button text-white font-medium py-2 px-4 rounded-lg transition-all duration-200"
                          >
                            Continue Journey
                          </button>
                        )}
                      </div>
                    )}
                  </div>

                  {progress?.ai_confirmed && (
                    <div className="mt-3 flex items-center text-green-400 text-sm">
                      <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                      </svg>
                      AI Confirmed
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </main>

      {/* Left Panel - Stories & Progress */}
      {showLeftPanel && (
        <div className="fixed inset-y-0 left-0 z-30 w-80 bg-black bg-opacity-30 backdrop-filter backdrop-blur-lg border-r border-purple-300 border-opacity-30 panel-slide-in-left">
          <div className="p-6">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-semibold text-white">Your Stories</h3>
              <button
                onClick={() => setShowLeftPanel(false)}
                className="p-1 rounded-lg bg-white bg-opacity-20 hover:bg-opacity-30 transition-all duration-200"
              >
                <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div className="space-y-4 max-h-96 overflow-y-auto">
              {userProgress.map((progress) => {
                const story = stories.find(s => s.id === progress.story_id);
                if (!story) return null;

                return (
                  <div
                    key={progress.id}
                    className="glass-effect rounded-lg p-4 cursor-pointer hover:bg-white hover:bg-opacity-10 transition-all duration-200"
                    onClick={() => setSelectedStory(story)}
                  >
                    <h4 className="text-white font-medium mb-2">{story.title}</h4>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-purple-300 text-sm">{progress.status}</span>
                      <span className="text-purple-300 text-sm">{progress.acceptance_level}%</span>
                    </div>
                    <div className="w-full bg-white bg-opacity-20 rounded-full h-1">
                      <div 
                        className={`h-1 rounded-full bg-gradient-to-r ${getProgressColor(progress.acceptance_level)}`}
                        style={{ width: `${progress.acceptance_level}%` }}
                      ></div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* Right Panel - Todo List */}
      {showRightPanel && (
        <div className="fixed inset-y-0 right-0 z-30 w-80 bg-black bg-opacity-30 backdrop-filter backdrop-blur-lg border-l border-purple-300 border-opacity-30 panel-slide-in-right">
          <div className="p-6">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-semibold text-white">Journey Tasks</h3>
              <button
                onClick={() => setShowRightPanel(false)}
                className="p-1 rounded-lg bg-white bg-opacity-20 hover:bg-opacity-30 transition-all duration-200"
              >
                <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div className="space-y-3 max-h-96 overflow-y-auto">
              {todos.length === 0 ? (
                <div className="text-center text-purple-300 py-8">
                  <svg className="w-12 h-12 mx-auto mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                  <p>No tasks yet. Start a journey to receive guidance.</p>
                </div>
              ) : (
                todos.map((todo) => (
                  <div
                    key={todo.id}
                    className={`glass-effect rounded-lg p-4 ${todo.completed ? 'opacity-60' : ''}`}
                  >
                    <div className="flex items-start">
                      <input
                        type="checkbox"
                        checked={todo.completed}
                        className="mt-1 mr-3 w-4 h-4 text-purple-600 rounded focus:ring-purple-500"
                        readOnly
                      />
                      <div className="flex-1">
                        <h4 className={`text-white font-medium mb-1 ${todo.completed ? 'line-through' : ''}`}>
                          {todo.title}
                        </h4>
                        <p className="text-purple-300 text-sm">{todo.description}</p>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}

      {/* Overlay for panels */}
      {(showLeftPanel || showRightPanel) && (
        <div
          className="fixed inset-0 bg-black bg-opacity-30 z-20"
          onClick={() => {
            setShowLeftPanel(false);
            setShowRightPanel(false);
          }}
        ></div>
      )}
    </div>
  );
};

export default Dashboard;
