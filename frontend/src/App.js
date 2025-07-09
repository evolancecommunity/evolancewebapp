import React, { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import axios from "axios";
import "./App.css";

// Import components
import SplashScreen from "./components/SplashScreen";
import Auth from "./components/Auth";
import OnboardingFlow from "./components/OnboardingFlow";
import Dashboard from "./components/Dashboard";
import Profile from "./components/Profile";
import ChatInterface from "./components/ChatInterface";
import PodcastLessons from "./components/PodcastLessons";
import ConsciousnessTimeline from "./components/ConsciousnessTimeline";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Auth Context
const AuthContext = React.createContext();

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showSplash, setShowSplash] = useState(true);

  useEffect(() => {
    checkAuthStatus();
    
    // Show splash screen for 3 seconds
    const splashTimer = setTimeout(() => {
      setShowSplash(false);
    }, 3000);

    return () => clearTimeout(splashTimer);
  }, []);

  const checkAuthStatus = async () => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const response = await axios.get(`${API}/auth/me`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setUser(response.data);
      } catch (error) {
        localStorage.removeItem('token');
      }
    }
    setLoading(false);
  };

  const login = async (email, password) => {
    try {
      const response = await axios.post(`${API}/auth/login`, {
        email,
        password
      });
      
      const { access_token } = response.data;
      localStorage.setItem('token', access_token);
      
      // Get user info
      const userResponse = await axios.get(`${API}/auth/me`, {
        headers: { Authorization: `Bearer ${access_token}` }
      });
      
      setUser(userResponse.data);
      return true;
    } catch (error) {
      console.error('Login error:', error);
      return false;
    }
  };

  const register = async (email, password, fullName) => {
    try {
      const response = await axios.post(`${API}/auth/register`, {
        email,
        password,
        full_name: fullName
      });
      
      const { access_token } = response.data;
      localStorage.setItem('token', access_token);
      
      // Get user info
      const userResponse = await axios.get(`${API}/auth/me`, {
        headers: { Authorization: `Bearer ${access_token}` }
      });
      
      setUser(userResponse.data);
      return true;
    } catch (error) {
      console.error('Registration error:', error);
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-700 to-indigo-800 flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-white"></div>
      </div>
    );
  }

  if (showSplash) {
    return <SplashScreen onComplete={() => setShowSplash(false)} />;
  }

  return (
    <AuthContext.Provider value={{ user, login, register, logout, API }}>
      <div className="App">
        <BrowserRouter>
          <Routes>
            {!user ? (
              <>
                <Route path="/auth" element={<Auth />} />
                <Route path="*" element={<Navigate to="/auth" replace />} />
              </>
            ) : !user.personality_test_completed ? (
              <>
                <Route path="/onboarding" element={<OnboardingFlow />} />
                <Route path="*" element={<Navigate to="/onboarding" replace />} />
              </>
            ) : (
              <>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/profile" element={<Profile />} />
                <Route path="/chat" element={<ChatInterface />} />
                <Route path="/podcasts" element={<PodcastLessons />} />
                <Route path="/consciousness" element={<ConsciousnessTimeline />} />
                <Route path="*" element={<Navigate to="/dashboard" replace />} />
              </>
            )}
          </Routes>
        </BrowserRouter>
      </div>
    </AuthContext.Provider>
  );
}

export default App;
export { AuthContext };
