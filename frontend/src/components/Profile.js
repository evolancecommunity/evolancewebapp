import React, { useContext, useState, useEffect } from 'react';
import { AuthContext } from '../App';
import { useNavigate } from 'react-router-dom';

const Profile = () => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const [isEditing, setIsEditing] = useState(false);
  const [profileData, setProfileData] = useState({
    full_name: user?.full_name || '',
    email: user?.email || ''
  });

  useEffect(() => {
    if (user) {
      setProfileData({
        full_name: user.full_name,
        email: user.email
      });
    }
  }, [user]);

  const handleInputChange = (e) => {
    setProfileData({
      ...profileData,
      [e.target.name]: e.target.value
    });
  };

  const handleSave = () => {
    // TODO: Implement profile update API call
    setIsEditing(false);
  };

  const getInitials = (name) => {
    return name?.split(' ').map(n => n[0]).join('').toUpperCase() || 'U';
  };

<<<<<<< HEAD
  const getSpiritualLevel = (level) => {
    if (level >= 90) return { name: 'Enlightened Soul', color: 'text-yellow-300' };
    if (level >= 80) return { name: 'Awakened Spirit', color: 'text-purple-300' };
    if (level >= 70) return { name: 'Conscious Being', color: 'text-blue-300' };
    if (level >= 60) return { name: 'Seeking Soul', color: 'text-green-300' };
    if (level >= 40) return { name: 'Growing Spirit', color: 'text-orange-300' };
    return { name: 'Beginning Journey', color: 'text-gray-300' };
  };

  const spiritualLevel = getSpiritualLevel(user?.spiritual_level || 0);

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-700 to-indigo-800 relative overflow-hidden">
      {/* Spiritual Background */}
      <div 
        className="absolute inset-0 opacity-30"
        style={{
          backgroundImage: `url('https://images.pexels.com/photos/1121123/pexels-photo-1121123.jpeg')`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          filter: 'blur(2px)'
        }}
      ></div>

      {/* Floating Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-20 left-20 w-32 h-32 bg-purple-400 rounded-full opacity-20 blur-xl animate-pulse float"></div>
        <div className="absolute bottom-32 right-16 w-48 h-48 bg-indigo-400 rounded-full opacity-20 blur-xl animate-pulse delay-1000 float"></div>
        <div className="absolute top-1/3 right-1/4 w-24 h-24 bg-purple-300 rounded-full opacity-20 blur-xl animate-pulse delay-500 float"></div>
        <div className="absolute bottom-1/4 left-1/3 w-36 h-36 bg-cyan-400 rounded-full opacity-20 blur-xl animate-pulse delay-300 float"></div>
      </div>

      {/* Header */}
      <header className="relative z-20 bg-black bg-opacity-20 backdrop-filter backdrop-blur-lg border-b border-purple-300 border-opacity-30">
=======
  const getWellbeingLevel = (level) => {
    if (level >= 90) return { name: 'Thriving', color: 'text-emerald-400', bg: 'bg-emerald-500/20' };
    if (level >= 80) return { name: 'Flourishing', color: 'text-blue-400', bg: 'bg-blue-500/20' };
    if (level >= 70) return { name: 'Growing', color: 'text-indigo-400', bg: 'bg-indigo-500/20' };
    if (level >= 60) return { name: 'Developing', color: 'text-purple-400', bg: 'bg-purple-500/20' };
    if (level >= 40) return { name: 'Building', color: 'text-orange-400', bg: 'bg-orange-500/20' };
    return { name: 'Beginning', color: 'text-slate-400', bg: 'bg-slate-500/20' };
  };

  const wellbeingLevel = getWellbeingLevel(user?.spiritual_level || 0);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Subtle Background Pattern */}
      <div className="absolute inset-0 opacity-5">
        <div className="absolute inset-0" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`
        }}></div>
      </div>

      {/* Header */}
      <header className="relative z-20 bg-slate-800/50 backdrop-blur-lg border-b border-slate-700/50">
>>>>>>> neel
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <button
              onClick={() => navigate('/dashboard')}
<<<<<<< HEAD
              className="flex items-center text-purple-200 hover:text-white transition-colors duration-200"
=======
              className="flex items-center text-slate-300 hover:text-white transition-colors duration-200"
>>>>>>> neel
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
<<<<<<< HEAD
              Back to Dashboard
            </button>

            <h1 className="text-2xl font-bold text-white">Spiritual Profile</h1>

            <button
              onClick={logout}
              className="p-2 rounded-lg bg-red-500 bg-opacity-30 hover:bg-opacity-50 transition-all duration-200"
            >
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
=======
              Dashboard
            </button>

            <h1 className="text-xl font-semibold text-white">Profile & Wellbeing</h1>

            <button
              onClick={logout}
              className="p-2 rounded-lg bg-red-500/20 hover:bg-red-500/30 transition-all duration-200"
            >
              <svg className="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
>>>>>>> neel
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="relative z-10 p-6">
        <div className="max-w-4xl mx-auto">
          {/* Profile Card */}
<<<<<<< HEAD
          <div className="glass-effect rounded-3xl p-8 md:p-12 spiritual-glow-strong mb-8">
            <div className="text-center">
              {/* 3D Profile Picture */}
              <div className="relative inline-block mb-8">
                {/* Outer Glow Ring */}
                <div className="absolute inset-0 rounded-full bg-gradient-to-r from-purple-400 to-cyan-400 animate-pulse blur-lg opacity-75"></div>
                
                {/* Middle Ring */}
                <div className="relative w-48 h-48 md:w-56 md:h-56 rounded-full bg-gradient-to-br from-purple-500 via-purple-600 to-indigo-700 p-2 transform hover:scale-105 transition-all duration-500">
                  {/* Inner Profile Circle */}
                  <div className="w-full h-full rounded-full bg-gradient-to-br from-purple-800 via-purple-900 to-indigo-900 flex items-center justify-center text-6xl md:text-7xl font-bold text-white profile-glow transform hover:rotate-3 transition-all duration-500">
=======
          <div className="bg-slate-800/50 backdrop-blur-lg border border-slate-700/50 rounded-2xl p-8 mb-8">
            <div className="text-center">
              {/* Profile Picture */}
              <div className="relative inline-block mb-8">
                <div className="w-32 h-32 md:w-40 md:h-40 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 p-1">
                  <div className="w-full h-full rounded-full bg-slate-800 flex items-center justify-center text-4xl md:text-5xl font-bold text-white">
>>>>>>> neel
                    {user?.profile_picture ? (
                      <img 
                        src={user.profile_picture} 
                        alt="Profile" 
                        className="w-full h-full rounded-full object-cover"
                      />
                    ) : (
<<<<<<< HEAD
                      <span className="gradient-text-light">{getInitials(user?.full_name)}</span>
                    )}
                  </div>

                  {/* Floating Spiritual Elements */}
                  <div className="absolute -top-4 -right-4 w-8 h-8 bg-yellow-400 rounded-full opacity-80 animate-bounce delay-75"></div>
                  <div className="absolute -bottom-4 -left-4 w-6 h-6 bg-cyan-400 rounded-full opacity-80 animate-bounce delay-150"></div>
                  <div className="absolute top-8 -left-6 w-4 h-4 bg-purple-300 rounded-full opacity-80 animate-bounce"></div>
                  <div className="absolute bottom-8 -right-6 w-5 h-5 bg-indigo-300 rounded-full opacity-80 animate-bounce delay-200"></div>
                </div>

                {/* Edit Button */}
                <button
                  onClick={() => setIsEditing(true)}
                  className="absolute bottom-4 right-4 w-12 h-12 bg-purple-600 hover:bg-purple-700 rounded-full flex items-center justify-center transition-all duration-200 spiritual-glow"
                >
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
=======
                      <span>{getInitials(user?.full_name)}</span>
                    )}
                  </div>
                </div>

                <button
                  onClick={() => setIsEditing(true)}
                  className="absolute bottom-2 right-2 w-10 h-10 bg-blue-600 hover:bg-blue-700 rounded-full flex items-center justify-center transition-all duration-200"
                >
                  <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
>>>>>>> neel
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>
              </div>

<<<<<<< HEAD
              {/* Name and Title */}
              <h2 className="text-4xl md:text-5xl font-bold text-white mb-4 scale-in">
=======
              {/* Name and Status */}
              <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
>>>>>>> neel
                {user?.full_name}
              </h2>
              
              <div className="mb-6">
<<<<<<< HEAD
                <span className={`text-2xl font-semibold ${spiritualLevel.color} slide-up`}>
                  {spiritualLevel.name}
                </span>
                <p className="text-purple-200 mt-2">Spiritual Level: {user?.spiritual_level || 0}</p>
              </div>

              {/* Spiritual Progress Bar */}
              <div className="max-w-md mx-auto mb-8">
                <div className="w-full bg-white bg-opacity-20 rounded-full h-3">
                  <div 
                    className="progress-bar h-3 rounded-full transition-all duration-1000 ease-out"
=======
                <span className={`text-lg font-semibold ${wellbeingLevel.color}`}>
                  {wellbeingLevel.name}
                </span>
                <p className="text-slate-400 mt-1">Wellbeing Level: {user?.spiritual_level || 0}</p>
              </div>

              {/* Wellbeing Progress Bar */}
              <div className="max-w-md mx-auto mb-8">
                <div className="w-full bg-slate-700 rounded-full h-3">
                  <div 
                    className="bg-gradient-to-r from-blue-500 to-purple-600 h-3 rounded-full transition-all duration-1000 ease-out"
>>>>>>> neel
                    style={{ width: `${(user?.spiritual_level || 0)}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>

          {/* Profile Details */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Personal Information */}
<<<<<<< HEAD
            <div className="glass-effect rounded-2xl p-6 spiritual-glow">
              <h3 className="text-2xl font-semibold text-white mb-6 flex items-center">
                <svg className="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
=======
            <div className="bg-slate-800/50 backdrop-blur-lg border border-slate-700/50 rounded-xl p-6">
              <h3 className="text-xl font-semibold text-white mb-6 flex items-center">
                <svg className="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
>>>>>>> neel
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                Personal Information
              </h3>

              {isEditing ? (
                <div className="space-y-4">
                  <div>
<<<<<<< HEAD
                    <label className="block text-purple-200 text-sm font-medium mb-2">Full Name</label>
=======
                    <label className="block text-slate-300 text-sm font-medium mb-2">Full Name</label>
>>>>>>> neel
                    <input
                      type="text"
                      name="full_name"
                      value={profileData.full_name}
                      onChange={handleInputChange}
<<<<<<< HEAD
                      className="w-full px-4 py-3 bg-white bg-opacity-10 border border-purple-300 border-opacity-30 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-400"
                    />
                  </div>
                  <div>
                    <label className="block text-purple-200 text-sm font-medium mb-2">Email</label>
=======
                      className="w-full px-4 py-3 bg-slate-700/50 border border-slate-600 text-slate-200 placeholder-slate-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label className="block text-slate-300 text-sm font-medium mb-2">Email</label>
>>>>>>> neel
                    <input
                      type="email"
                      name="email"
                      value={profileData.email}
                      onChange={handleInputChange}
<<<<<<< HEAD
                      className="w-full px-4 py-3 bg-white bg-opacity-10 border border-purple-300 border-opacity-30 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-400"
=======
                      className="w-full px-4 py-3 bg-slate-700/50 border border-slate-600 text-slate-200 placeholder-slate-400 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
>>>>>>> neel
                    />
                  </div>
                  <div className="flex space-x-3">
                    <button
                      onClick={handleSave}
<<<<<<< HEAD
                      className="flex-1 spiritual-button text-white font-medium py-2 px-4 rounded-lg"
=======
                      className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors duration-200"
>>>>>>> neel
                    >
                      Save Changes
                    </button>
                    <button
                      onClick={() => setIsEditing(false)}
<<<<<<< HEAD
                      className="flex-1 bg-gray-600 hover:bg-gray-700 text-white font-medium py-2 px-4 rounded-lg transition-all duration-200"
=======
                      className="px-4 py-2 bg-slate-600 hover:bg-slate-700 text-white font-medium rounded-lg transition-colors duration-200"
>>>>>>> neel
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  <div>
<<<<<<< HEAD
                    <span className="text-purple-300 text-sm">Full Name</span>
                    <p className="text-white text-lg">{user?.full_name}</p>
                  </div>
                  <div>
                    <span className="text-purple-300 text-sm">Email</span>
                    <p className="text-white text-lg">{user?.email}</p>
                  </div>
                  <div>
                    <span className="text-purple-300 text-sm">Member Since</span>
                    <p className="text-white text-lg">
                      {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
                    </p>
                  </div>
                  <div>
                    <span className="text-purple-300 text-sm">Account Status</span>
                    <p className="text-green-400 text-lg">Active</p>
                  </div>
=======
                    <label className="block text-slate-400 text-sm font-medium mb-1">Full Name</label>
                    <p className="text-white">{user?.full_name}</p>
                  </div>
                  <div>
                    <label className="block text-slate-400 text-sm font-medium mb-1">Email</label>
                    <p className="text-white">{user?.email}</p>
                  </div>
                  <div>
                    <label className="block text-slate-400 text-sm font-medium mb-1">Member Since</label>
                    <p className="text-white">
                      {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'Recently'}
                    </p>
                  </div>
>>>>>>> neel
                </div>
              )}
            </div>

<<<<<<< HEAD
            {/* Spiritual Achievements */}
            <div className="glass-effect rounded-2xl p-6 spiritual-glow">
              <h3 className="text-2xl font-semibold text-white mb-6 flex items-center">
                <svg className="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                Spiritual Journey
              </h3>

              <div className="space-y-6">
                <div className="text-center">
                  <div className="text-4xl font-bold text-white mb-2">{user?.spiritual_level || 0}</div>
                  <div className="text-purple-300">Enlightenment Points</div>
                </div>

                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-purple-300">Personality Assessment</span>
                    <span className="text-green-400">✓ Complete</span>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-purple-300">Stories Started</span>
                    <span className="text-white">3</span>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-purple-300">Stories Completed</span>
                    <span className="text-white">1</span>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-purple-300">AI Sessions</span>
                    <span className="text-white">12</span>
                  </div>
                </div>

                <div className="pt-4 border-t border-purple-300 border-opacity-30">
                  <h4 className="text-lg font-semibold text-white mb-3">Recent Achievements</h4>
                  <div className="space-y-2">
                    <div className="flex items-center text-purple-200">
                      <span className="text-yellow-400 mr-2">🏆</span>
                      First Steps on the Path
                    </div>
                    <div className="flex items-center text-purple-200">
                      <span className="text-purple-400 mr-2">💜</span>
                      Spiritual Awareness Unlocked
                    </div>
                    <div className="flex items-center text-purple-200">
                      <span className="text-blue-400 mr-2">🧘</span>
                      Inner Peace Seeker
                    </div>
=======
            {/* Wellbeing Stats */}
            <div className="bg-slate-800/50 backdrop-blur-lg border border-slate-700/50 rounded-xl p-6">
              <h3 className="text-xl font-semibold text-white mb-6 flex items-center">
                <svg className="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                Wellbeing Insights
              </h3>

              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-slate-700/30 rounded-lg">
                  <div>
                    <p className="text-slate-300 text-sm">Current Level</p>
                    <p className="text-white font-semibold">{wellbeingLevel.name}</p>
                  </div>
                  <div className={`w-12 h-12 ${wellbeingLevel.bg} rounded-full flex items-center justify-center`}>
                    <span className="text-2xl">💙</span>
                  </div>
                  </div>
                  
                <div className="flex items-center justify-between p-4 bg-slate-700/30 rounded-lg">
                  <div>
                    <p className="text-slate-300 text-sm">Sessions Completed</p>
                    <p className="text-white font-semibold">24</p>
                  </div>
                  <div className="w-12 h-12 bg-blue-500/20 rounded-full flex items-center justify-center">
                    <span className="text-2xl">📊</span>
                  </div>
                </div>

                <div className="flex items-center justify-between p-4 bg-slate-700/30 rounded-lg">
                  <div>
                    <p className="text-slate-300 text-sm">Streak</p>
                    <p className="text-white font-semibold">7 days</p>
                    </div>
                  <div className="w-12 h-12 bg-emerald-500/20 rounded-full flex items-center justify-center">
                    <span className="text-2xl">🔥</span>
>>>>>>> neel
                  </div>
                </div>
              </div>
            </div>
          </div>

<<<<<<< HEAD
          {/* Action Buttons */}
          <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={() => navigate('/chat')}
              className="spiritual-button text-white font-semibold py-3 px-8 rounded-lg transition-all duration-200"
            >
              Continue Spiritual Journey
            </button>
            <button
              onClick={() => navigate('/videos')}
              className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 px-8 rounded-lg transition-all duration-200"
            >
              Explore Video Lessons
            </button>
=======
          {/* Recent Activity */}
          <div className="mt-8 bg-slate-800/50 backdrop-blur-lg border border-slate-700/50 rounded-xl p-6">
            <h3 className="text-xl font-semibold text-white mb-6 flex items-center">
              <svg className="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Recent Activity
            </h3>

            <div className="space-y-4">
              {[
                { type: 'chat', message: 'Completed emotional support session', time: '2 hours ago' },
                { type: 'checkin', message: 'Responded to wellbeing check-in', time: '1 day ago' },
                { type: 'reflection', message: 'Added journal entry', time: '2 days ago' },
                { type: 'progress', message: 'Reached new wellbeing milestone', time: '1 week ago' }
              ].map((activity, index) => (
                <div key={index} className="flex items-center space-x-4 p-4 bg-slate-700/30 rounded-lg">
                  <div className="w-10 h-10 bg-blue-500/20 rounded-full flex items-center justify-center">
                    <span className="text-lg">
                      {activity.type === 'chat' ? '💬' : 
                       activity.type === 'checkin' ? '💙' : 
                       activity.type === 'reflection' ? '📝' : '🎯'}
                    </span>
                  </div>
                  <div className="flex-1">
                    <p className="text-white text-sm">{activity.message}</p>
                    <p className="text-slate-400 text-xs">{activity.time}</p>
                  </div>
                </div>
              ))}
            </div>
>>>>>>> neel
          </div>
        </div>
      </main>
    </div>
  );
};

export default Profile;
