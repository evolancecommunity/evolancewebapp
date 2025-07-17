import React, { useEffect, useState } from 'react';

const SplashScreen = ({ onComplete }) => {
  const [fadeOut, setFadeOut] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setFadeOut(true);
      setTimeout(onComplete, 500);
    }, 2500);

    return () => clearTimeout(timer);
  }, [onComplete]);

  return (
    <div className={`fixed inset-0 bg-gradient-to-br from-purple-900 via-purple-700 to-indigo-800 flex flex-col items-center justify-center transition-opacity duration-500 ${fadeOut ? 'opacity-0' : 'opacity-100'}`}>
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute top-20 left-20 w-32 h-32 bg-purple-400 rounded-full blur-xl animate-pulse"></div>
        <div className="absolute bottom-32 right-16 w-48 h-48 bg-indigo-400 rounded-full blur-xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-purple-300 rounded-full blur-2xl animate-pulse delay-500"></div>
      </div>

      {/* Logo Container */}
      <div className="relative z-10 flex flex-col items-center">
        {/* Infinity Symbol */}
        <div className="mb-8 infinity-glow">
          <svg
            width="120"
            height="60"
            viewBox="0 0 120 60"
            className="animate-pulse"
          >
            <path
              d="M20,30 C20,20 30,10 40,10 C50,10 60,20 60,30 C60,20 70,10 80,10 C90,10 100,20 100,30 C100,40 90,50 80,50 C70,50 60,40 60,30 C60,40 50,50 40,50 C30,50 20,40 20,30 Z"
              fill="none"
              stroke="white"
              strokeWidth="3"
              className="drop-shadow-lg"
            />
            <defs>
              <linearGradient id="infinityGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#a78bfa" />
                <stop offset="50%" stopColor="#ffffff" />
                <stop offset="100%" stopColor="#c084fc" />
              </linearGradient>
            </defs>
            <path
              d="M20,30 C20,20 30,10 40,10 C50,10 60,20 60,30 C60,20 70,10 80,10 C90,10 100,20 100,30 C100,40 90,50 80,50 C70,50 60,40 60,30 C60,40 50,50 40,50 C30,50 20,40 20,30 Z"
              fill="url(#infinityGradient)"
              className="animate-pulse"
            />
          </svg>
        </div>

        {/* App Name */}
        <h1 className="text-6xl md:text-7xl font-bold text-white mb-4 scale-in">
          <span className="gradient-text-light">Evolance</span>
        </h1>

        {/* Tagline */}
        <p className="text-xl md:text-2xl text-purple-200 text-center max-w-md slide-up opacity-90">
          Transform your soul, embrace your journey
        </p>

        {/* Spiritual Elements */}
        <div className="mt-12 flex space-x-4">
          <div className="w-2 h-2 bg-purple-300 rounded-full animate-ping"></div>
          <div className="w-2 h-2 bg-purple-300 rounded-full animate-ping delay-75"></div>
          <div className="w-2 h-2 bg-purple-300 rounded-full animate-ping delay-150"></div>
        </div>
      </div>

      {/* Bottom Glow */}
      <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-96 h-32 bg-gradient-to-t from-purple-600 to-transparent opacity-50 blur-xl"></div>
    </div>
  );
};

export default SplashScreen;
