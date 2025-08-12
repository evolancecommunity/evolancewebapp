import React, { useState, useEffect, useContext, useRef } from 'react';
import { AuthContext } from '../App';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
<<<<<<< HEAD
=======
import CrisisAlert from './CrisisAlert';
>>>>>>> neel

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [recognition, setRecognition] = useState(null);
<<<<<<< HEAD
=======
  const [showCrisisAlert, setShowCrisisAlert] = useState(false);
  const [chatMode, setChatMode] = useState('support'); // support, therapy, reflection
  const [learningStatus, setLearningStatus] = useState(null);
  const [modelUsed, setModelUsed] = useState('gemini');
>>>>>>> neel
  const messagesEndRef = useRef(null);

  const { user, API } = useContext(AuthContext);
  const navigate = useNavigate();
  const location = useLocation();
  const storyContext = location.state?.storyContext;

  useEffect(() => {
    fetchChatHistory();
    initializeVoiceRecognition();
    return () => {
      if (recognition) {
        recognition.stop();
      }
    };
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const fetchChatHistory = async () => {
    try {
      const token = localStorage.getItem('token');
      const params = storyContext ? `?story_context=${storyContext}` : '';
      const response = await axios.get(`${API}/chat/history${params}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setMessages(response.data);
    } catch (error) {
      console.error('Error fetching chat history:', error);
    }
  };

  const initializeVoiceRecognition = () => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognitionInstance = new SpeechRecognition();
      
      recognitionInstance.continuous = false;
      recognitionInstance.interimResults = false;
      recognitionInstance.lang = 'en-US';

      recognitionInstance.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInputMessage(transcript);
        setIsListening(false);
      };

      recognitionInstance.onerror = () => {
        setIsListening(false);
      };

      recognitionInstance.onend = () => {
        setIsListening(false);
      };

      setRecognition(recognitionInstance);
    }
  };

  const startVoiceRecognition = () => {
    if (recognition) {
      setIsListening(true);
      recognition.start();
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || loading) return;

    const userMessage = {
      id: Date.now().toString(),
      user_id: user.id,
      message: inputMessage,
      is_user: true,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    const messageToSend = inputMessage;
    setInputMessage('');
    setLoading(true);

    try {
      const token = localStorage.getItem('token');
<<<<<<< HEAD
      const response = await axios.post(`${API}/chat/message`, 
        `message=${encodeURIComponent(messageToSend)}${storyContext ? `&story_context=${storyContext}` : ''}`,
        {
          headers: { 
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/x-www-form-urlencoded'
=======
      const response = await axios.post(`${API}/ai/gemini-chat`, 
        { message: messageToSend },
        {
          headers: { 
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
>>>>>>> neel
          }
        }
      );

<<<<<<< HEAD
      setMessages(prev => [...prev, response.data]);
=======
      // Create AI response message with emotion analysis
      const aiMessage = {
        id: Date.now().toString(),
        user_id: 'ai',
        message: response.data.response,
        is_user: false,
        timestamp: new Date().toISOString(),
        emotionAnalysis: response.data.emotion_analysis,
        emolyticsUpdate: response.data.emolytics_update,
        modelUsed: response.data.model_used
      };

      setMessages(prev => [...prev, aiMessage]);
      
      // Update learning status
      if (response.data.learning_status) {
        setLearningStatus(response.data.learning_status);
      }
      
      // Update model used
      if (response.data.model_used) {
        setModelUsed(response.data.model_used);
      }
      
      // Log emolytics update for debugging
      if (response.data.emolytics_update) {
        console.log('Emolytics updated:', response.data.emolytics_update);
      }
      
>>>>>>> neel
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, {
        id: Date.now().toString(),
        user_id: 'system',
<<<<<<< HEAD
        message: 'Sorry, I encountered an error. Please try again.',
=======
        message: 'I apologize, but I\'m having trouble processing your message right now. Please try again in a moment.',
>>>>>>> neel
        is_user: false,
        timestamp: new Date().toISOString()
      }]);
    }

    setLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

<<<<<<< HEAD
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-700 to-indigo-800 relative overflow-hidden">
      {/* Moving Galaxy Background */}
      <div className="absolute inset-0 moving-galaxy-bg">
        {/* Primary Galaxy Layer */}
        <div className="absolute inset-0 opacity-30">
          <div className="galaxy-spiral galaxy-spiral-1"></div>
          <div className="galaxy-spiral galaxy-spiral-2"></div>
          <div className="galaxy-spiral galaxy-spiral-3"></div>
        </div>
        
        {/* Floating Stars */}
        <div className="absolute inset-0 overflow-hidden">
          {[...Array(50)].map((_, i) => (
            <div
              key={i}
              className="absolute w-1 h-1 bg-white rounded-full opacity-60 animate-twinkle"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 5}s`,
                animationDuration: `${2 + Math.random() * 3}s`
              }}
            ></div>
          ))}
        </div>

        {/* Flowing Energy Streams */}
        <div className="absolute inset-0">
          <div className="energy-stream energy-stream-1"></div>
          <div className="energy-stream energy-stream-2"></div>
          <div className="energy-stream energy-stream-3"></div>
        </div>

        {/* Cosmic Dust Clouds */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="cosmic-dust cosmic-dust-1"></div>
          <div className="cosmic-dust cosmic-dust-2"></div>
          <div className="cosmic-dust cosmic-dust-3"></div>
          <div className="cosmic-dust cosmic-dust-4"></div>
        </div>
      </div>

      {/* Header */}
      <header className="relative z-20 bg-black bg-opacity-30 backdrop-filter backdrop-blur-lg border-b border-purple-300 border-opacity-30">
=======
  const getChatModeIcon = (mode) => {
    switch (mode) {
      case 'support': return '💙';
      case 'therapy': return '🧠';
      case 'reflection': return '✨';
      default: return '💬';
    }
  };

  const getChatModeLabel = (mode) => {
    switch (mode) {
      case 'support': return 'Emotional Support';
      case 'therapy': return 'Therapeutic Dialogue';
      case 'reflection': return 'Self-Reflection';
      default: return 'Chat';
    }
  };

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

            <div className="text-center">
              <h1 className="text-2xl font-bold text-white">Chat with Evolance</h1>
              <p className="text-purple-200 text-sm">Your AI spiritual guide</p>
            </div>

            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
              <span className="text-purple-200 text-sm">Online</span>
=======
              Dashboard
            </button>

            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <span className="text-2xl">{getChatModeIcon(chatMode)}</span>
                <h1 className="text-xl font-semibold text-white">{getChatModeLabel(chatMode)}</h1>
              </div>
              
              {/* Learning Status Indicator */}
              {learningStatus && (
                <div className="flex items-center space-x-2 px-3 py-1 bg-slate-700/50 rounded-lg border border-slate-600/50">
                  <div className={`w-2 h-2 rounded-full ${
                    modelUsed === 'trained' ? 'bg-emerald-500' : 'bg-blue-500'
                  }`}></div>
                  <span className="text-xs text-slate-300">
                    {modelUsed === 'trained' ? 'Trained AI' : 'Gemini AI'}
                  </span>
                  <div className="text-xs text-slate-400">
                    ({learningStatus.total_interactions} interactions)
                  </div>
                </div>
              )}
            </div>

            <div className="flex items-center space-x-3">
              <select
                value={chatMode}
                onChange={(e) => setChatMode(e.target.value)}
                className="bg-slate-700/50 border border-slate-600 text-slate-200 text-sm rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="support">Emotional Support</option>
                <option value="therapy">Therapeutic Dialogue</option>
                <option value="reflection">Self-Reflection</option>
              </select>
>>>>>>> neel
            </div>
          </div>
        </div>
      </header>

      {/* Chat Container */}
<<<<<<< HEAD
      <div className="relative z-10 flex flex-col h-screen pt-20">
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto px-4 py-6">
          <div className="max-w-4xl mx-auto space-y-6">
            {/* Welcome Message */}
            {messages.length === 0 && (
              <div className="text-center py-12">
                <div className="inline-block mb-6">
                  <svg width="80" height="40" viewBox="0 0 120 60" className="infinity-glow">
                    <defs>
                      <linearGradient id="chatInfinityGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stopColor="#a78bfa" />
                        <stop offset="50%" stopColor="#ffffff" />
                        <stop offset="100%" stopColor="#c084fc" />
                      </linearGradient>
                    </defs>
                    <path
                      d="M20,30 C20,20 30,10 40,10 C50,10 60,20 60,30 C60,20 70,10 80,10 C90,10 100,20 100,30 C100,40 90,50 80,50 C70,50 60,40 60,30 C60,40 50,50 40,50 C30,50 20,40 20,30 Z"
                      fill="url(#chatInfinityGradient)"
                    />
                  </svg>
                </div>
                <h2 className="text-3xl font-bold text-white mb-4">Welcome to Evolance</h2>
                <p className="text-purple-200 text-lg max-w-2xl mx-auto">
                  I'm here to guide you on your spiritual journey. Share your thoughts, ask questions, 
                  or simply reflect on your experiences. Everything shared here is in confidence.
=======
      <div className="relative z-10 flex flex-col h-[calc(100vh-80px)]">
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-6">
          <div className="max-w-4xl mx-auto space-y-6">
            {messages.length === 0 && (
              <div className="text-center py-12">
                <div className="w-16 h-16 bg-blue-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-white mb-2">Welcome to your emotional support space</h3>
                <p className="text-slate-400 max-w-md mx-auto">
                  I'm here to provide compassionate support, therapeutic guidance, and help you explore your emotional wellbeing. 
                  How are you feeling today?
>>>>>>> neel
                </p>
              </div>
            )}

<<<<<<< HEAD
            {/* Chat Messages */}
            {messages.map((message, index) => (
              <div
                key={message.id || index}
                className={`message-appear flex ${message.is_user ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`max-w-xs md:max-w-md lg:max-w-lg px-6 py-4 rounded-2xl ${
                  message.is_user
                    ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white ml-auto'
                    : 'glass-effect text-white spiritual-glow'
                }`}>
                  {!message.is_user && (
                    <div className="flex items-center mb-2">
                      <div className="w-8 h-8 bg-gradient-to-r from-purple-400 to-cyan-400 rounded-full flex items-center justify-center mr-3">
                        <span className="text-white text-sm font-bold">E</span>
                      </div>
                      <span className="text-purple-300 text-sm font-medium">Evolance</span>
                    </div>
                  )}
                  <p className="text-white leading-relaxed whitespace-pre-wrap">{message.message}</p>
                  <div className={`text-xs mt-2 ${message.is_user ? 'text-purple-200' : 'text-purple-300'}`}>
                    {formatTimestamp(message.timestamp)}
                  </div>
                </div>
              </div>
            ))}

            {/* Loading Message */}
            {loading && (
              <div className="flex justify-start">
                <div className="glass-effect px-6 py-4 rounded-2xl spiritual-glow">
                  <div className="flex items-center mb-2">
                    <div className="w-8 h-8 bg-gradient-to-r from-purple-400 to-cyan-400 rounded-full flex items-center justify-center mr-3">
                      <span className="text-white text-sm font-bold">E</span>
                    </div>
                    <span className="text-purple-300 text-sm font-medium">Evolance</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce delay-75"></div>
                    <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce delay-150"></div>
                    <span className="text-purple-200 ml-2">Contemplating...</span>
=======
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.is_user ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`max-w-[70%] ${message.is_user ? 'order-2' : 'order-1'}`}>
                  <div className={`rounded-2xl px-6 py-4 ${
                  message.is_user
                      ? 'bg-blue-600 text-white' 
                      : 'bg-slate-700/50 text-slate-200 border border-slate-600/50'
                }`}>
                    <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.message}</p>
                    <div className={`text-xs mt-2 ${
                      message.is_user ? 'text-blue-200' : 'text-slate-400'
                    }`}>
                      {formatTimestamp(message.timestamp)}
                    </div>
                  </div>
                  
                  {/* Emotion Analysis Display */}
                  {!message.is_user && message.emotionAnalysis && (
                    <div className="mt-3 p-4 bg-slate-800/50 border border-slate-600/30 rounded-xl">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center">
                          <span className="text-emerald-400 mr-2">🧠</span>
                          <span className="text-sm font-medium text-slate-300">Emotion Analysis</span>
                        </div>
                        {message.modelUsed && (
                          <div className="flex items-center space-x-1">
                            <div className={`w-2 h-2 rounded-full ${
                              message.modelUsed === 'trained' ? 'bg-emerald-500' : 'bg-blue-500'
                            }`}></div>
                            <span className="text-xs text-slate-400">
                              {message.modelUsed === 'trained' ? 'Trained' : 'Gemini'}
                            </span>
                          </div>
                        )}
                      </div>
                      <div className="space-y-2">
                        <div className="flex justify-between items-center">
                          <span className="text-xs text-slate-400">Primary Emotion:</span>
                          <span className="text-xs font-medium text-emerald-300 capitalize">
                            {message.emotionAnalysis.primary_emotion}
                          </span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-xs text-slate-400">Intensity:</span>
                          <div className="flex items-center">
                            <div className="w-16 h-2 bg-slate-600 rounded-full mr-2">
                              <div 
                                className="h-2 bg-emerald-500 rounded-full transition-all duration-300"
                                style={{ width: `${message.emotionAnalysis.emotion_intensity}%` }}
                              ></div>
                            </div>
                            <span className="text-xs text-slate-300">
                              {message.emotionAnalysis.emotion_intensity}%
                            </span>
                          </div>
                        </div>
                        {message.emotionAnalysis.secondary_emotions && message.emotionAnalysis.secondary_emotions.length > 0 && (
                          <div className="flex justify-between items-center">
                            <span className="text-xs text-slate-400">Secondary:</span>
                            <span className="text-xs text-slate-300">
                              {message.emotionAnalysis.secondary_emotions.join(', ')}
                            </span>
                          </div>
                        )}
                        {message.emotionAnalysis.reasoning && (
                          <div className="mt-2 p-2 bg-slate-700/30 rounded text-xs text-slate-300">
                            <span className="text-slate-400">Reasoning: </span>
                            {message.emotionAnalysis.reasoning}
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
                
                {!message.is_user && (
                  <div className="order-1 mr-3">
                    <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                      <span className="text-white font-semibold text-sm">AI</span>
                    </div>
                  </div>
                )}
              </div>
            ))}

            {loading && (
              <div className="flex justify-start">
                <div className="order-1 mr-3">
                  <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                    <span className="text-white font-semibold text-sm">AI</span>
                  </div>
                </div>
                <div className="order-2">
                  <div className="bg-slate-700/50 border border-slate-600/50 rounded-2xl px-6 py-4">
                    <div className="flex space-x-2">
                      <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                      <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                    </div>
>>>>>>> neel
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Area */}
<<<<<<< HEAD
        <div className="relative z-20 bg-black bg-opacity-30 backdrop-filter backdrop-blur-lg border-t border-purple-300 border-opacity-30 px-4 py-6">
          <div className="max-w-4xl mx-auto">
            <div className="flex items-end space-x-4">
              {/* Voice Input Button */}
              {recognition && (
                <button
                  onClick={startVoiceRecognition}
                  disabled={isListening || loading}
                  className={`p-3 rounded-full transition-all duration-200 ${
                    isListening 
                      ? 'bg-red-500 hover:bg-red-600 animate-pulse' 
                      : 'bg-purple-600 hover:bg-purple-700'
                  } disabled:opacity-50 disabled:cursor-not-allowed`}
                  title={isListening ? 'Listening...' : 'Voice Input'}
                >
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                  </svg>
                </button>
              )}

              {/* Text Input */}
              <div className="flex-1">
=======
        <div className="border-t border-slate-700/50 bg-slate-800/30 backdrop-blur-lg p-6">
          <div className="max-w-4xl mx-auto">
            <div className="flex items-end space-x-4">
              <div className="flex-1 relative">
>>>>>>> neel
                <textarea
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
<<<<<<< HEAD
                  placeholder="Share your thoughts with Evolance..."
                  disabled={loading}
                  className="w-full px-6 py-4 bg-white bg-opacity-10 border border-purple-300 border-opacity-30 rounded-2xl text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent transition-all duration-200 resize-none disabled:opacity-50"
                  rows="2"
                />
              </div>

              {/* Send Button */}
              <button
                onClick={sendMessage}
                disabled={!inputMessage.trim() || loading}
                className="p-4 spiritual-button rounded-full disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
                title="Send Message"
              >
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
=======
                  placeholder="Share your thoughts, feelings, or concerns..."
                  className="w-full px-4 py-3 bg-slate-700/50 border border-slate-600 text-slate-200 placeholder-slate-400 rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  rows="1"
                  style={{ minHeight: '48px', maxHeight: '120px' }}
                />
                <div className="absolute bottom-2 right-2 text-slate-500 text-xs">
                  {inputMessage.length}/1000
                </div>
              </div>
              
              <div className="flex items-center space-x-2">
                <button
                  onClick={startVoiceRecognition}
                  disabled={isListening}
                  className={`p-3 rounded-xl transition-all duration-200 ${
                    isListening 
                      ? 'bg-red-500 text-white' 
                      : 'bg-slate-700/50 text-slate-300 hover:bg-slate-600/50 hover:text-white'
                  }`}
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                  </svg>
                </button>
                
              <button
                onClick={sendMessage}
                disabled={!inputMessage.trim() || loading}
                  className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 disabled:cursor-not-allowed text-white font-medium rounded-xl transition-all duration-200 flex items-center space-x-2"
              >
                  <span>Send</span>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
>>>>>>> neel
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </button>
            </div>
<<<<<<< HEAD

            {/* Voice Recognition Feedback */}
            {isListening && (
              <div className="mt-4 text-center">
                <p className="text-purple-200 text-sm">🎤 Listening... Speak now</p>
              </div>
            )}

            {/* Story Context Indicator */}
            {storyContext && (
              <div className="mt-4 text-center">
                <div className="inline-flex items-center px-4 py-2 bg-purple-600 bg-opacity-30 rounded-full">
                  <svg className="w-4 h-4 mr-2 text-purple-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                  <span className="text-purple-200 text-sm">Discussing your current story</span>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
=======
              </div>
            
            <div className="mt-3 flex items-center justify-between text-xs text-slate-500">
              <span>Your conversations are private and secure</span>
              <span>Press Enter to send, Shift+Enter for new line</span>
              </div>
          </div>
        </div>
      </div>

      {/* Crisis Alert */}
      {showCrisisAlert && (
        <CrisisAlert onClose={() => setShowCrisisAlert(false)} />
      )}
>>>>>>> neel
    </div>
  );
};

export default ChatInterface;
